from __future__ import annotations

import math

import pandas as pd


CINEMA_GRADE_SCORES = {
    "A+": 100,
    "A": 95,
    "A-": 90,
    "B+": 80,
    "B": 70,
    "B-": 60,
    "C+": 50,
    "C": 40,
    "C-": 30,
    "D+": 0,
    "D": 0,
    "D-": 0,
    "F": 0,
}

REQUIRED_COLUMNS = {
    "date",
    "title",
    "box_office_rank",
    "daily_gross",
    "total_gross",
    "days_in_release",
    "cinema_grade",
    "critic_score",
}


def cinema_grade_to_score(grade: str | float | None) -> float:
    """Convert CinemaScore-style grades to a numeric score."""
    if grade is None or pd.isna(grade):
        return 0.0
    return float(CINEMA_GRADE_SCORES.get(str(grade).strip().upper(), 0))


def rank_multiplier(box_office_rank: int | float | None) -> float:
    """Top-10 rank bonus used by the recovered local project."""
    if box_office_rank is None or pd.isna(box_office_rank):
        return 1.0

    rank = int(box_office_rank)
    if rank < 1 or rank > 10:
        return 1.0
    return 1 + (10 - rank) / 9


def performance_score(
    total_gross: float,
    daily_gross: float,
    box_office_rank: int,
    max_base_points: float = 50.0,
) -> float:
    """Score daily box-office momentum from cumulative gross growth."""
    previous_total = total_gross - daily_gross
    if previous_total <= 0:
        return 0.0

    growth_pct = (daily_gross / previous_total) * 100
    if growth_pct < 0:
        return 0.0

    base_points = min(math.sqrt(growth_pct), max_base_points)
    return base_points * rank_multiplier(box_office_rank)


def score_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a ranked Movie League table from movie-level signal data."""
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_cols}")

    scored = frame.copy()
    scored["previous_total_gross"] = scored["total_gross"] - scored["daily_gross"]
    scored["daily_growth_pct"] = (
        scored["daily_gross"] / scored["previous_total_gross"].replace(0, pd.NA)
    ) * 100
    scored["cinema_score"] = scored["cinema_grade"].apply(cinema_grade_to_score)
    scored["rank_multiplier"] = scored["box_office_rank"].apply(rank_multiplier)
    scored["performance_score"] = scored.apply(
        lambda row: performance_score(
            total_gross=row["total_gross"],
            daily_gross=row["daily_gross"],
            box_office_rank=row["box_office_rank"],
        ),
        axis=1,
    )
    scored["game_score"] = (
        scored["cinema_score"] + scored["critic_score"] + scored["performance_score"]
    )

    scored = scored.sort_values(
        ["game_score", "daily_gross"], ascending=[False, False]
    ).reset_index(drop=True)
    scored.insert(0, "league_rank", scored.index + 1)
    return scored

