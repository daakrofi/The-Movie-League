# Scoring Method

Movie League was designed as a lightweight ranking system for films currently in release. The recovered local project joined three signals:

- Box-office momentum from daily gross and cumulative gross.
- CinemaScore-style audience grades mapped to numeric points.
- Critic score, represented here as a Rotten Tomatoes-style percentage field.

The portfolio version keeps the scoring logic but removes local database credentials and private runtime state.

## Performance Score

The recovered performance score used cumulative box-office growth:

```text
previous_total_gross = total_gross - daily_gross
daily_growth_pct = daily_gross / previous_total_gross * 100
base_points = sqrt(daily_growth_pct), capped at 50
rank_multiplier = 1 + (10 - box_office_rank) / 9 for ranks 1 through 10
performance_score = base_points * rank_multiplier
```

This rewards strong daily momentum while tapering the bonus across the top 10 box-office positions.

## Game Score

```text
game_score = cinema_score + critic_score + performance_score
```

The final table is sorted by `game_score`, with daily gross as a tie-breaker.

