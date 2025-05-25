## Data Dictionary: `fact_top_performer_by_points` table.

| # | column_name | data_type | nullable | description                                                                      | constraints | example                          |
|---|-------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1 | season_sk   | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2 | player_sk   | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | 5b3e1c7f8a2d4e69b3f2c1234567890a |
| 3 | points      | int       | No       | Total number of points scored by the player                                      |             | 45                               |

