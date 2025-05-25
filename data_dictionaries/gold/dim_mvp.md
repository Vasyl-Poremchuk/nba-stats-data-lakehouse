## Data Dictionary: `dim_mvp` table

| # | column_name | data_type | nullable | description                                                                | constraints                  | example                          |
|---|-------------|-----------|----------|----------------------------------------------------------------------------|------------------------------|----------------------------------|
| 1 | season_sk   | string    | No       | Surrogate key generate using MD5 hash of the season (e.g., `2023-24`)      | PK (part of a composite key) | a2780b07486e1c62d89fbe93fdff1a3b |
| 2 | mvp_sk      | string    | No       | Surrogate key generate using MD5 hash of the player name (e.g., `J.Tatum`) | PK (part of a composite key) | 7dcae8bf8bfbe88fcfc7b31abcfffbdc |
| 3 | mvp         | string    | No       | Full name of the player who won the MVP award for the season               |                              | L. Bird                          |
