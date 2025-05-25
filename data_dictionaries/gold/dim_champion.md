## Data Dictionary: `dim_champion` table.

| # | column_name | data_type | nullable | description                                                            | constraints                  | example                          |
|---|-------------|-----------|----------|------------------------------------------------------------------------|------------------------------|----------------------------------|
| 1 | season_sk   | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`) | PK (part of a composite key) | 637b6e2af1a35bb7d533803ee1a7ddd8 |
| 2 | team_sk     | string    | No       | Surrogate key generated using MD5 hash of the team name                | PK (part of a composite key) | 8ef4ac08814f3de3bff92300d69f940a |
| 3 | champion    | string    | No       | Name of the team that won the championship for the given season        |                              | Milwaukee Bucks                  |
