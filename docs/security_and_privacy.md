# Security and Privacy

This repository is a sanitized portfolio version of a local analytics project.

- No hard-coded credentials are included.
- `.env` files, database files, logs, raw scrape dumps, and private data folders are ignored.
- `.env.example` contains placeholder values only.
- The included sample is small and intended for reproducible demonstration.

Before adding new connectors, keep credentials in local environment variables or a secret manager, not in Python files or notebooks.

