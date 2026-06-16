import pandas as pd

from movie_league.scoring import (
    cinema_grade_to_score,
    performance_score,
    rank_multiplier,
    score_frame,
)


def test_cinema_grade_mapping_handles_known_and_missing_values():
    assert cinema_grade_to_score("A+") == 100
    assert cinema_grade_to_score("b-") == 60
    assert cinema_grade_to_score(None) == 0
    assert cinema_grade_to_score("unknown") == 0


def test_rank_multiplier_tapers_across_top_ten():
    assert rank_multiplier(1) == 2.0
    assert rank_multiplier(10) == 1.0
    assert rank_multiplier(11) == 1.0


def test_performance_score_uses_growth_and_rank_bonus():
    score = performance_score(total_gross=120, daily_gross=20, box_office_rank=1)
    assert round(score, 2) == 8.94


def test_score_frame_returns_ranked_table():
    frame = pd.DataFrame(
        [
            {
                "date": "2025-07-20",
                "title": "Movie A",
                "box_office_rank": 1,
                "daily_gross": 20,
                "total_gross": 120,
                "days_in_release": 2,
                "cinema_grade": "A",
                "critic_score": 80,
            },
            {
                "date": "2025-07-20",
                "title": "Movie B",
                "box_office_rank": 5,
                "daily_gross": 10,
                "total_gross": 100,
                "days_in_release": 4,
                "cinema_grade": "B",
                "critic_score": 40,
            },
        ]
    )

    ranked = score_frame(frame)

    assert ranked.loc[0, "title"] == "Movie A"
    assert ranked.loc[0, "league_rank"] == 1
    assert "game_score" in ranked.columns

