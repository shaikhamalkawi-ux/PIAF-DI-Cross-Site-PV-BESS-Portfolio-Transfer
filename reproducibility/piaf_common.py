"""Shared deterministic calculations for the R6R8 clean-room replays."""

from __future__ import annotations

import hashlib
import itertools
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


ETA = math.sqrt(0.90)
TOLERANCE = 1e-12
QUANTILES = {
    "3x3": (0.50, 0.75, 0.90),
    "5x5": (0.25, 0.50, 0.75, 0.90, 0.95),
}
FROZEN = {
    "3x3": ("E50-P50", "E75-P50", "E75-P75", "E90-P50"),
    "5x5": ("E25-P25", "E50-P25", "E50-P75", "E75-P25"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def quantile_label(value: float) -> str:
    return str(int(round(100 * value)))


def pareto_requirements(rows: Sequence[dict]) -> list[dict]:
    eligible = [row for row in rows if row["g_pp"] > 0.0]
    result: list[dict] = []
    for candidate in eligible:
        dominated = any(
            other["g_pp"] >= candidate["g_pp"] - TOLERANCE
            and other["E_kWh"] <= candidate["E_kWh"] + TOLERANCE
            and other["P_kW"] <= candidate["P_kW"] + TOLERANCE
            and (
                other["g_pp"] > candidate["g_pp"] + TOLERANCE
                or other["E_kWh"] < candidate["E_kWh"] - TOLERANCE
                or other["P_kW"] < candidate["P_kW"] - TOLERANCE
            )
            for other in eligible
            if other is not candidate
        )
        if not dominated:
            result.append(candidate)
    return result


def point_epsilon(requirement: dict, candidate: dict) -> float:
    return max(
        0.0,
        1.0 - candidate["g_pp"] / requirement["g_pp"],
        candidate["E_kWh"] / requirement["E_kWh"] - 1.0,
        candidate["P_kW"] / requirement["P_kW"] - 1.0,
    )


def portfolio_loss(requirements: Sequence[dict], portfolio: Sequence[dict]) -> float:
    return max(
        min(point_epsilon(requirement, candidate) for candidate in portfolio)
        for requirement in requirements
    )


def exact_portfolio_summary(rows: Sequence[dict], grid: str, k: int = 4) -> dict:
    requirements = pareto_requirements(rows)
    universe = list(itertools.combinations(rows, k))
    frozen = [next(row for row in rows if row["label"] == label) for label in FROZEN[grid]]
    transferred = portfolio_loss(requirements, frozen)
    losses = np.asarray([portfolio_loss(requirements, selection) for selection in universe])
    best_index = int(np.argmin(losses))
    best = float(losses[best_index])
    beaten = int(np.sum(losses > transferred))
    return {
        "k": k,
        "n_requirements": len(requirements),
        "same_budget_percentile_pct": 100.0 * beaten / len(universe),
        "transferred_loss_pct": 100.0 * transferred,
        "local_floor_pct": 100.0 * best,
        "selection_excess_pp": 100.0 * (transferred - best),
        "n_exact_subsets": len(universe),
        "beaten_subsets": beaten,
        "best_local_set": "/".join(row["label"] for row in universe[best_index]),
        "frozen_set": "/".join(FROZEN[grid]),
        "descriptive_5pct_state": (
            "representation_budget_limit"
            if best > 0.05
            else "selection_excess"
            if transferred > 0.05
            else "low_transferred"
        ),
        "max_incremental_battery_benefit_pp": max(row["g_pp"] for row in rows),
    }


def unconstrained_daily_duties(
    load: np.ndarray,
    pv: np.ndarray,
    dates: np.ndarray,
    calibration_dates: Iterable,
    dt_hours: float,
) -> tuple[list[float], list[float]]:
    energy_duties: list[float] = []
    power_duties: list[float] = []
    for day in calibration_dates:
        stored = 0.0
        energy_duty = 0.0
        power_duty = 0.0
        for demand, generation in zip(load[dates == day], pv[dates == day]):
            surplus = max(generation - demand, 0.0)
            deficit = max(demand - generation, 0.0)
            charge = surplus
            discharge = min(deficit, ETA * stored)
            stored += ETA * charge - discharge / ETA
            energy_duty = max(energy_duty, stored)
            power_duty = max(power_duty, charge / dt_hours, discharge / dt_hours)
        energy_duties.append(energy_duty)
        power_duties.append(power_duty)
    return energy_duties, power_duties


def dispatch_candidate(
    load: np.ndarray,
    pv: np.ndarray,
    dates: np.ndarray,
    holdout_dates: Iterable,
    energy_kwh: float,
    power_kw: float,
    dt_hours: float,
) -> tuple[float, float, float, float]:
    total_load = 0.0
    grid_energy = 0.0
    pv_only_grid_energy = 0.0
    max_violation = 0.0
    for day in holdout_dates:
        stored = 0.0
        for demand, generation in zip(load[dates == day], pv[dates == day]):
            surplus = max(generation - demand, 0.0)
            deficit = max(demand - generation, 0.0)
            charge = min(surplus, power_kw * dt_hours, max(0.0, (energy_kwh - stored) / ETA))
            discharge = min(deficit, power_kw * dt_hours, ETA * stored)
            stored += ETA * charge - discharge / ETA
            max_violation = max(max_violation, -stored, stored - energy_kwh, 0.0)
            total_load += demand
            grid_energy += deficit - discharge
            pv_only_grid_energy += deficit
    rho = 100.0 * (1.0 - grid_energy / total_load)
    rho_pv = 100.0 * (1.0 - pv_only_grid_energy / total_load)
    return rho - rho_pv, rho, rho_pv, max_violation
