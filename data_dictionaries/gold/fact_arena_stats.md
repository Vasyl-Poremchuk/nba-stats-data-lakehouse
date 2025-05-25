## Data Dictionary: `fact_arena_stats` table.

| # | column_name         | data_type | nullable | description                                                                        | constraints | example                          |
|---|---------------------|-----------|----------|------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1 | season_sk           | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)             | FK          | 28aefe7f1e18c3d24f93304d4ee52aa3 |
| 2 | team_sk             | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)    | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3 | arena_sk            | string    | No       | Surrogate key generated using MD5 hash of the arena name (e.g., `Milwaukee Arena`) | FK          | 3547412cb302a61f1803b757149795bb |
| 4 | attendance          | int       | Yes      | Total number of attendees across all home games in the given season                |             | 785396                           |
| 5 | attendance_per_game | int       | Yes      | Average attendance per home game during the season                                 |             | 19156                            |
