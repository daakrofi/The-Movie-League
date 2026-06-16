# Data Sources

The sample dataset uses a small recovered snapshot of the domestic box office table saved locally for July 20, 2025. It includes title, daily gross, cumulative gross, days in release, and box-office rank.

CinemaScore and critic score fields are included as small demonstration fields so the scoring pipeline can run end to end without publishing private local database state. In a production version, those signals would be loaded from licensed or approved public sources and cached with source timestamps.

No raw scraped HTML, browser caches, local database files, or large datasets are included in this repository.

