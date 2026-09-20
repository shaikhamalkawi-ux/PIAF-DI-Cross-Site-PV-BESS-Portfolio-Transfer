"""Replay the R6R8 SlimPark branches from the official 4TU workbooks."""

from __future__ import annotations

import argparse
import json
import math
import tempfile
import zipfile
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


EXPECTED = {
    "zip": "84bc48f1fe7631e52c431b6da117b2f55bf2fbbfa5f9c150757c2818f53f9a78",
    "README.txt": "e09dca3d738e17cdbcdcc4165d73c4776673bc301eef83fbafa374b64aa9523e",
    "data.xlsx": "6ad935224d7fff3da5afaea3dfc0d98df9f6fdd63f7cb3a4773b5b5ba104b698",
    "transactions.xlsx": "d005d11418732425cf0aa712d8eca9d70357493f166135b9aca991712960d42d",
}


def source_directory(args: argparse.Namespace, temporary_directory: str) -> Path:
    if args.source_zip:
        if sha256_file(args.source_zip) != EXPECTED["zip"]:
            raise ValueError("SlimPark ZIP SHA-256 does not match the locked official source")
        with zipfile.ZipFile(args.source_zip) as archive:
            archive.extractall(temporary_directory)
        return Path(temporary_directory)
    if args.source_dir:
        return args.source_dir
    raise ValueError("provide --source-zip or --source-dir")


def read_source(root: Path) -> tuple[pd.DataFrame, dict]:
    for name in ("README.txt", "data.xlsx", "transactions.xlsx"):
        path = root / name
        if not path.exists() or sha256_file(path) != EXPECTED[name]:
            raise ValueError(f"missing or hash-mismatched source file: {name}")
    data = pd.read_excel(root / "data.xlsx", sheet_name="Slimpark 2022-2023")
    transactions = pd.read_excel(root / "transactions.xlsx")
    data["time"] = pd.to_datetime(data["time"], utc=True)
    evse = [f"evse_{index}_wh" for index in range(1, 10)]
    time_diff = data["time"].sort_values().diff().dropna().dt.total_seconds()
    qa = {
        "zip_sha256": EXPECTED["zip"],
        "readme_sha256": EXPECTED["README.txt"],
        "data_xlsx_sha256": EXPECTED["data.xlsx"],
        "transactions_xlsx_sha256": EXPECTED["transactions.xlsx"],
        "data_rows": len(data),
        "transaction_rows": len(transactions),
        "time_min": str(data["time"].min()),
        "time_max": str(data["time"].max()),
        "duplicate_times": int(data["time"].duplicated().sum()),
        "hourly_cadence_non1h_intervals": int((time_diff != 3600).sum()),
        "negative_evse_values": int((data[evse] < 0).sum().sum()),
        "positive_pv_wh_values": int((data["pv_wh"] > 0).sum()),
        "last_nonmissing_pv_time": str(data.loc[data["pv_wh"].notna(), "time"].max()),
        "battery_monitoring": "README states 30-kWh Kiwatt Power Pack with 15-kW inverter was not monitored",
    }
    return data, qa


def admitted_series(data: pd.DataFrame, columns: list[str]) -> dict:
    frame = data[(data["time"] >= "2022-05-20") & (data["time"] < "2023-11-24")].copy()
    frame["date"] = frame["time"].dt.date
    accepted = []
    for day, group in frame.groupby("date", sort=True):
        if len(group) != 24 or group[columns + ["pv_wh"]].isna().any().any():
            continue
        if group[columns].to_numpy(float).sum() <= 0.0:
            continue
        accepted.append(day)
    frame = frame[frame["date"].isin(accepted)].sort_values("time")
    load = frame[columns].sum(axis=1).to_numpy(float) / 1000.0
    native_pv = -frame["pv_wh"].to_numpy(float) / 1000.0
    dates = np.asarray(frame["date"])
    ncal = math.floor(0.70 * len(accepted))
    calibration = accepted[:ncal]
    holdout = accepted[ncal:]
    return {
        "load": load,
        "native_pv": native_pv,
        "dates": dates,
        "calibration": calibration,
        "holdout": holdout,
        "accepted": accepted,
    }


def metadata(series: dict, scale: float) -> dict:
    dates = series["dates"]
    cal_mask = np.isin(dates, series["calibration"])
    hold_mask = np.isin(dates, series["holdout"])
    return {
        "pv_scale": scale,
        "complete_active_days": len(series["accepted"]),
        "cal_days": len(series["calibration"]),
        "hold_days": len(series["holdout"]),
        "first_admitted_day": str(series["accepted"][0]),
        "last_admitted_day": str(series["accepted"][-1]),
        "cal_ev_kwh": float(series["load"][cal_mask].sum()),
        "cal_pv_kwh_native": float(series["native_pv"][cal_mask].sum()),
        "hold_ev_kwh": float(series["load"][hold_mask].sum()),
        "hold_pv_kwh_native": float(series["native_pv"][hold_mask].sum()),
    }


def replay_variant(subset: str, scale_mode: str, data: pd.DataFrame) -> tuple[list[dict], list[dict], list[dict], dict]:
    columns = [f"evse_{index}_wh" for index in range(1, 10 if subset == "all9" else 5)]
    series = admitted_series(data, columns)
    cal_mask = np.isin(series["dates"], series["calibration"])
    native_cal_pv = series["native_pv"][cal_mask].sum()
    scale = 1.0 if scale_mode == "native" else series["load"][cal_mask].sum() / native_cal_pv
    pv = series["native_pv"] * scale
    meta = metadata(series, scale)
    base = {"subset": subset, "pv_scale_mode": scale_mode, **meta}
    quantile_rows: list[dict] = []
    response_rows: list[dict] = []
    summary_rows: list[dict] = []
    e_duties, p_duties = unconstrained_daily_duties(
        series["load"], pv, series["dates"], series["calibration"], 1.0
    )
    for grid, levels in QUANTILES.items():
        energies = {q: round(float(np.quantile(e_duties, q)), 3) for q in levels}
        powers = {q: round(float(np.quantile(p_duties, q)), 3) for q in levels}
        for axis, values, unit in (("E", energies, "kWh"), ("P", powers, "kW")):
            for q, value in values.items():
                quantile_rows.append({**base, "grid": grid, "axis": axis, "quantile": q, "value": value, "unit": unit})
        candidates: list[dict] = []
        for qe in levels:
            for qp in levels:
                label = f"E{quantile_label(qe)}-P{quantile_label(qp)}"
                gain, rho, rho_pv, violation = dispatch_candidate(
                    series["load"], pv, series["dates"], series["holdout"], energies[qe], powers[qp], 1.0
                )
                candidates.append({
                    "subset": subset,
                    "pv_scale_mode": scale_mode,
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
        response_rows.extend(candidates)
        summary_rows.append({**base, "grid": grid, **exact_portfolio_summary(candidates, grid)})
    return quantile_rows, response_rows, summary_rows, base


def compare_numeric(got: pd.DataFrame, expected: pd.DataFrame, keys: list[str]) -> tuple[int, float]:
    merged = expected.merge(got, on=keys, how="outer", suffixes=("_expected", "_got"), indicator=True)
    missing = int((merged["_merge"] != "both").sum())
    max_diff = 0.0
    for name in expected.columns:
        if name in keys or name not in got.columns:
            continue
        left = f"{name}_expected"
        right = f"{name}_got"
        if pd.api.types.is_numeric_dtype(expected[name]) and not pd.api.types.is_bool_dtype(expected[name]):
            values = (pd.to_numeric(merged[left], errors="coerce") - pd.to_numeric(merged[right], errors="coerce")).abs()
            if values.notna().any():
                max_diff = max(max_diff, float(values.max()))
        else:
            missing += int((merged[left].astype(str) != merged[right].astype(str)).sum())
    return missing, max_diff


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", type=Path)
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reference-dir", type=Path, default=Path(__file__).parent / "reference" / "derived")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="piaf_slimpark_") as temporary:
        source = source_directory(args, temporary)
        data, qa = read_source(source)
        quantiles: list[dict] = []
        responses: list[dict] = []
        summaries: list[dict] = []
        admissions: list[dict] = []
        for subset, mode in (("all9", "native"), ("first4", "native"), ("all9", "energy_matched")):
            q, r, s, a = replay_variant(subset, mode, data)
            quantiles.extend(q)
            responses.extend(r)
            summaries.extend(s)
            admissions.append(a)
    qdf = pd.DataFrame(quantiles)
    rdf = pd.DataFrame(responses)
    sdf = pd.DataFrame(summaries)
    adf = pd.DataFrame(admissions)
    primary = sdf[(sdf["subset"] == "all9") & (sdf["pv_scale_mode"] == "native")].copy()
    qdf.to_csv(args.output_dir / "slimpark_candidate_quantiles.csv", index=False)
    rdf.to_csv(args.output_dir / "slimpark_candidate_responses.csv", index=False)
    primary.to_csv(args.output_dir / "slimpark_primary_results.csv", index=False)
    sdf.to_csv(args.output_dir / "slimpark_all_branch_results.csv", index=False)
    adf.to_csv(args.output_dir / "slimpark_admission_support.csv", index=False)
    (args.output_dir / "slimpark_source_qa.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    checks = []
    comparisons = (
        ("quantiles", qdf, "slimpark_candidate_quantiles.csv", ["subset", "pv_scale_mode", "grid", "axis", "quantile"]),
        ("responses", rdf, "slimpark_candidate_responses.csv", ["subset", "pv_scale_mode", "grid", "label"]),
        ("primary", primary, "slimpark_primary_results.csv", ["subset", "pv_scale_mode", "grid"]),
        ("admission", adf, "slimpark_admission_support.csv", ["subset", "pv_scale_mode"]),
    )
    for name, got, filename, keys in comparisons:
        expected = pd.read_csv(args.reference_dir / filename)
        mismatches, max_diff = compare_numeric(got, expected, keys)
        checks.append({"check": name, "row_or_text_mismatches": mismatches, "max_abs_numeric_difference": max_diff, "status": "PASS" if mismatches == 0 and max_diff <= 1e-7 else "FAIL"})
    checks.append({"check": "official_source_hashes", "row_or_text_mismatches": 0, "max_abs_numeric_difference": 0.0, "status": "PASS"})
    verification = pd.DataFrame(checks)
    verification.to_csv(args.output_dir / "R6R8_SLIMPARK_VERIFICATION.csv", index=False)
    if (verification["status"] != "PASS").any():
        raise SystemExit("SlimPark replay differs from the locked reference tables")
    print(verification.to_string(index=False))


if __name__ == "__main__":
    main()
