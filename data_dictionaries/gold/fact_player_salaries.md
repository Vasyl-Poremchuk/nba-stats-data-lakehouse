## Data Dictionary: `fact_player_salaries` table.

| # | column_name | data_type | nullable | description                                                                      | constraints | example                          |
|---|-------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1 | season_sk   | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 0c1b198624c9263cdc946d02e83e4a24 |
| 2 | team_sk     | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | 5452e84700b026429276de4e8e6931df |
| 3 | player_sk   | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | f3a5c81e37b42f109e09b0d123456789 |
| 4 | rank        | int       | No       | Player’s rank by salary within the team                                          |             | 1                                |
| 5 | salary      | int       | Yes      | Player’s salary in US dollars                                                    |             | 15000000                         |


