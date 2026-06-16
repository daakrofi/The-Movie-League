from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from movie_league import score_frame


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA = ROOT / "data" / "sample" / "movie_signals_sample.csv"
OUTPUT_CSV = ROOT / "data" / "processed" / "sample_rankings.csv"
OUTPUT_FIGURE = ROOT / "reports" / "figures" / "sample_league_scores.png"


def main() -> None:
    frame = pd.read_csv(SAMPLE_DATA)
    ranked = score_frame(frame)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(OUTPUT_CSV, index=False)

    top = ranked.head(10).sort_values("game_score", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["title"], top["game_score"], color="#22577a")
    ax.set_title("Movie League Sample Rankings")
    ax.set_xlabel("Game score")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()

    OUTPUT_FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FIGURE, dpi=160)

    print(ranked[["league_rank", "title", "game_score", "performance_score"]])
    print(f"\nWrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_FIGURE}")


if __name__ == "__main__":
    main()

