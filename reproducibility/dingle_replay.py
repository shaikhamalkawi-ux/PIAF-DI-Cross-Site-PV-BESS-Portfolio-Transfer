"""Replay the R6R8 Dingle measured-PV branches from the public source CSVs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

from piaf_common import (
    FROZEN,
    QUANTILES,
    dispatch_candidate,
    exact_portfolio_summary,
    pareto_requirements,
    quantile_label,
    sha256_file,
    unconstrained_daily_duties,
)


def allocate_events(events: pd.DataFrame, index: pd.DatetimeIndex, event_mode: str) -> tuple[np.ndarray, float]:
    load = np.zeros(len(index), dtype=float)
    first_timestamp = index[0]
    max_residual = 0.0
    for event in events.itertuples(index=False):
        start = event.start_time
        end = event.end_time if event_mode == "event_window" else start + pd.to_timedelta(event.charge_seconds, unit="s")
        duration_hours = (end - start).total_seconds() / 3600.0
        first = max(0, int(math.floor((start - first_timestamp).total_seconds() / 1800.0)))
        last = min(len(index) - 1, int(math.ceil((end - first_timestamp).total_seconds() / 1800.0)) - 1)
        allocated: list[tuple[int, float]] = []
        for position in range(first, last + 1):
            left = index[position]
            right = left + pd.Timedelta(minutes=30)
            overlap_hours = max(0.0, (min(end, right) - max(start, left)).total_seconds() / 3600.0)
            if overlap_hours:
                allocated.append((position, event.energy * overlap_hours / duration_hours))
        before = sum(value for _, value in allocated)
        max_residual = max(max_residual, abs(event.energy - before))
        if allocated:
            position, value = allocated[-1]
            allocated[-1] = (position, value + event.energy - before)
        for position, value in allocated:
            load[position] += value
    return load, max_residual


def clean_pv(raw: pd.Series, article_aligned: bool) -> pd.Series:
    pv = pd.to_numeric(raw, errors="coerce").copy()
    if article_aligned:
        pv[(pv < 0.0) | (pv > 1.05)] = np.nan
        return pv.interpolate(method="linear", limit=3, limit_area="inside")
    return pv


def load_household(source: Path, household: str) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    pv_frame = pd.read_csv(source / "EnergyStreams" / f"{household}_merged_30min.csv")
    pv_frame["timestamp"] = pd.to_datetime(pv_frame["timestamp"], utc=True)
    pv_frame = pv_frame.sort_values("timestamp").drop_duplicates("timestamp").set_index("timestamp")
    events = pd.read_csv(source / "JourneyCharge" / f"{household}_Sorted_Mobility.csv")
    events = events[events["event_type"].eq("charging")].copy()
    events["start_time"] = pd.to_datetime(events["start_time"], utc=True, errors="coerce")
    events["end_time"] = pd.to_datetime(events["end_time"], utc=True, errors="coerce")
    events["energy"] = pd.to_numeric(events["ENERGY"], errors="coerce")
    events["charge_seconds"] = pd.to_timedelta(events["CHARGING_TIME"], errors="coerce").dt.total_seconds()
    events["avg_kw"] = events["energy"] / (events["charge_seconds"] / 3600.0)
    valid_time = events["start_time"].notna() & events["end_time"].notna() & (events["end_time"] > events["start_time"])
    positive = events["energy"].notna() & (events["energy"] > 0.0)
    generic = events[valid_time & positive].copy()
    aligned = generic[(generic["energy"] <= 64.0) & (generic["avg_kw"] <= 7.4)].copy()
    raw_pv = pd.to_numeric(pv_frame["solar_kWh"], errors="coerce")
    quality = {
        "household": household,
        "raw_charging_events": len(events),
        "generic_valid_events": len(generic),
        "article_aligned_events": len(aligned),
        "nonpositive_or_missing_energy": int((~positive).sum()),
        "energy_gt_64_kwh": int((generic["energy"] > 64.0).sum()),
        "active_power_gt_7p4_kw": int(((generic["energy"] <= 64.0) & (generic["avg_kw"] > 7.4)).sum()),
        "max_energy_kwh": float(generic["energy"].max()),
        "max_active_avg_kw": float(aligned["avg_kw"].max()),
        "pv_rows": len(pv_frame),
        "pv_missing_raw": int(raw_pv.isna().sum()),
        "pv_negative_raw": int((raw_pv < 0.0).sum()),
        "pv_above_1p05_kwh_raw": int((raw_pv > 1.05).sum()),
        "pv_min_raw_kwh": float(raw_pv.min()),
        "pv_max_raw_kwh": float(raw_pv.max()),
    }
    return pv_frame, events, quality


def replay_variant(source: Path, household: str, article_aligned: bool, pv_mode: str, event_mode: str):
    pv_frame, all_events, quality = load_household(source, household)
    valid_time = all_events["start_time"].notna() & all_events["end_time"].notna() & (all_events["end_time"] > all_events["start_time"])
    positive = all_events["energy"].notna() & (all_events["energy"] > 0.0)
    events = all_events[valid_time & positive].copy()
    if article_aligned:
        events = events[(events["energy"] <= 64.0) & (events["avg_kw"] <= 7.4)].copy()
    load, residual = allocate_events(events, pv_frame.index, event_mode)
    pv_series = clean_pv(pv_frame["solar_kWh"], article_aligned)
    dates = np.asarray(pv_frame.index.date)
    active_dates = sorted(set(dates[load > 0.0]))
    active_dates = [day for day in active_dates if np.all(np.isfinite(pv_series.to_numpy(float)[dates == day]))]
    ncal = math.floor(0.70 * len(active_dates))
    calibration = active_dates[:ncal]
    holdout = active_dates[ncal:]
    pv = pv_series.to_numpy(float)
    calibration_mask = np.isin(dates, calibration)
    scale = 1.0 if pv_mode == "native" else load[calibration_mask].sum() / pv[calibration_mask].sum()
    pv = pv * scale
    quality.update({
        "article_aligned": article_aligned,
        "max_reconstruction_residual_kwh": residual,
        "pv_missing_after_article_alignment": int(pd.isna(pv_series).sum()),
        "active_days": len(active_dates),
        "cal_days": len(calibration),
        "hold_days": len(holdout),
        "admitted_energy_kwh": float(events["energy"].sum()),
        "event_mode": event_mode,
        "pv_mode": pv_mode,
        "pv_scale": scale,
    })
    e_duties, p_duties = unconstrained_daily_duties(load, pv, dates, calibration, 0.5)
    quantiles: list[dict] = []
    responses: list[dict] = []
    summaries: list[dict] = []
    for grid, levels in QUANTILES.items():
        energies = {q: round(float(np.quantile(e_duties, q)), 3) for q in levels}
        powers = {q: round(float(np.quantile(p_duties, q)), 3) for q in levels}
        for axis, values, unit in (("E", energies, "kWh"), ("P", powers, "kW")):
            for quantile, value in values.items():
                quantiles.append({**quality, "grid": grid, "axis": axis, "quantile": quantile, "value": value, "unit": unit})
        candidates: list[dict] = []
        for qe in levels:
            for qp in levels:
                label = f"E{quantile_label(qe)}-P{quantile_label(qp)}"
                gain, rho, rho_pv, violation = dispatch_candidate(load, pv, dates, holdout, energies[qe], powers[qp], 0.5)
                candidates.append({
                    "household": household,
                    "article_aligned": article_aligned,
                    "pv_mode": pv_mode,
                    "event_mode": event_mode,
                    "grid": grid,
                    "qe": qe,
                    "qp": qp,
                    "label": label,
                    "E_kWh": energies[qe],
                    "P_kW": powers[qp],
                    "g_pp": gain,
                    "rho_pct": rho,
                    "rho_pv_pct": rho_pv,
                    "dispatch_violation": violation,
                    "is_frozen": label in FROZEN[grid],
                })
        pareto_labels = {row["label"] for row in pareto_requirements(candidates)}
        for row in candidates:
            row["is_pareto"] = row["label"] in pareto_labels
        responses.extend(candidates)
        summaries.append({**quality, "grid": grid, **exact_portfolio_summary(candidates, grid)})
    return quantiles, responses, summaries, quality


def verify_source(source: Path, reference: Path) -> list[dict]:
    checks = []
    for row in pd.read_csv(reference / "dingle_source_manifest.csv").itertuples(index=False):
        path = source / row.file
        actual = sha256_file(path) if path.exists() else "MISSING"
        checks.append({"check": f"source:{row.household}:{row.role}", "status": "PASS" if actual == row.sha256 else "FAIL", "max_abs_numeric_difference": 0.0, "row_or_text_mismatches": int(actual != row.sha256)})
    return checks


def compare_numeric(got: pd.DataFrame, expected: pd.DataFrame, keys: list[str]) -> tuple[int, float]:
    merged = expected.merge(got, on=keys, how="outer", suffixes=("_expected", "_got"), indicator=True)
    mismatches = int((merged["_merge"] != "both").sum())
    max_diff = 0.0
    for name in expected.columns:
        if name in keys or name not in got.columns:
            continue
        left, right = f"{name}_expected", f"{name}_got"
        if pd.api.types.is_numeric_dtype(expected[name]) and not pd.api.types.is_bool_dtype(expected[name]):
            difference = (pd.to_numeric(merged[left], errors="coerce") - pd.to_numeric(merged[right], errors="coerce")).abs()
            if difference.notna().any():
                max_diff = max(max_diff, float(difference.max()))
        else:
            mismatches += int((merged[left].astype(str) != merged[right].astype(str)).sum())
    return mismatches, max_diff


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True, help="Dingle Dataset directory containing RawData, EnergyStreams, and JourneyCharge")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reference-dir", type=Path, default=Path(__file__).parent / "reference" / "derived")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    quantiles: list[dict] = []
    responses: list[dict] = []
    summaries: list[dict] = []
    quality_rows: list[dict] = []
    variants = (
        (True, "native", "event_window"),
        (False, "native", "event_window"),
        (True, "energy_matched", "event_window"),
        (True, "native", "active_time_frontloaded"),
    )
    for household in ("id01", "id02", "id03", "id04"):
        for article_aligned, pv_mode, event_mode in variants:
            q, r, s, quality = replay_variant(args.source_dir, household, article_aligned, pv_mode, event_mode)
            quantiles.extend(q)
            responses.extend(r)
            summaries.extend(s)
            quality_rows.append(quality)
    qdf = pd.DataFrame(quantiles)
    rdf = pd.DataFrame(responses)
    sdf = pd.DataFrame(summaries)
    quality = pd.DataFrame(quality_rows)
    primary = sdf[(sdf["article_aligned"]) & (sdf["pv_mode"] == "native") & (sdf["event_mode"] == "event_window")]
    primary3 = primary[primary["grid"] == "3x3"].copy()
    primary5 = primary[primary["grid"] == "5x5"].copy()
    qdf.to_csv(args.output_dir / "dingle_candidate_quantiles.csv", index=False)
    rdf.to_csv(args.output_dir / "dingle_candidate_responses.csv", index=False)
    primary3.to_csv(args.output_dir / "dingle_primary_3x3_results.csv", index=False)
    primary5.to_csv(args.output_dir / "dingle_primary_5x5_results.csv", index=False)
    sdf.to_csv(args.output_dir / "dingle_all_branch_results.csv", index=False)
    quality.to_csv(args.output_dir / "dingle_source_quality_and_admission.csv", index=False)
    checks = verify_source(args.source_dir, args.reference_dir)
    comparisons = (
        ("quantiles", qdf, "dingle_candidate_quantiles.csv", ["household", "article_aligned", "pv_mode", "event_mode", "grid", "axis", "quantile"]),
        ("responses", rdf, "dingle_candidate_responses.csv", ["household", "article_aligned", "pv_mode", "event_mode", "grid", "label"]),
        ("primary_3x3", primary3, "dingle_primary_3x3_results.csv", ["household", "article_aligned", "pv_mode", "event_mode", "grid"]),
        ("primary_5x5", primary5, "dingle_primary_5x5_results.csv", ["household", "article_aligned", "pv_mode", "event_mode", "grid"]),
        ("source_quality", quality, "dingle_source_quality_and_admission.csv", ["household", "article_aligned", "pv_mode", "event_mode"]),
    )
    for name, got, filename, keys in comparisons:
        expected = pd.read_csv(args.reference_dir / filename)
        mismatches, max_diff = compare_numeric(got, expected, keys)
        checks.append({"check": name, "status": "PASS" if mismatches == 0 and max_diff <= 1e-7 else "FAIL", "max_abs_numeric_difference": max_diff, "row_or_text_mismatches": mismatches})
    verification = pd.DataFrame(checks)
    verification.to_csv(args.output_dir / "R6R8_DINGLE_VERIFICATION.csv", index=False)
    if (verification["status"] != "PASS").any():
        print(verification.to_string(index=False))
        raise SystemExit("Dingle replay differs from the locked reference tables")
    print(verification.to_string(index=False))


if __name__ == "__main__":
    main()
