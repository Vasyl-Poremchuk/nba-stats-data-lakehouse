## Data Dictionary: `fact_playoffs_per_36_minutes_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                      | constraints | example                          |
|----|---------------------------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 0c1b198624c9263cdc946d02e83e4a24 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | 7a4d13b6f24fcd2e4bafc8d7d35c1eaf |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | d9e7b1b4b5a1e56f1e2e8d7312345678 |
| 4  | rank                            | int       | No       | Player’s rank by playoff performance per 36 minutes                              |             | 12                               |
| 5  | games                           | int       | No       | Number of playoff games played                                                   |             | 20                               |
| 6  | games_started                   | int       | Yes      | Number of playoff games started                                                  |             | 20                               |
| 7  | minutes_played                  | int       | No       | Total minutes played in playoffs                                                 |             | 700                              |
| 8  | field_goals                     | double    | Yes      | Field goals made per 36 minutes                                                  |             | 8.5                              |
| 9  | field_goal_attempts             | double    | Yes      | Field goal attempts per 36 minutes                                               |             | 18.3                             |
| 10 | field_goal_percentage           | double    | Yes      | Field goal shooting percentage per 36 minutes                                    |             | 46.4                             |
| 11 | 3_point_field_goals             | double    | Yes      | 3-point field goals made per 36 minutes                                          |             | 2.3                              |
| 12 | 3_point_field_goal_attempts     | double    | Yes      | 3-point field goal attempts per 36 minutes                                       |             | 6.2                              |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | 3-point shooting percentage per 36 minutes                                       |             | 37.1                             |
| 14 | 2_point_field_goals             | double    | Yes      | 2-point field goals made per 36 minutes                                          |             | 6.2                              |
| 15 | 2_point_field_goal_attempts     | double    | Yes      | 2-point field goal attempts per 36 minutes                                       |             | 12.1                             |
| 16 | 2_point_field_gola_percentage   | double    | Yes      | 2-point shooting percentage per 36 minutes                                       |             | 51.2                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage per 36 minutes                                   |             | 52.3                             |
| 18 | free_throws                     | double    | Yes      | Free throws made per 36 minutes                                                  |             | 5.0                              |
| 19 | free_throw_attempts             | double    | Yes      | Free throw attempts per 36 minutes                                               |             | 6.1                              |
| 20 | free_throw_percentage           | double    | Yes      | Free throw shooting percentage per 36 minutes                                    |             | 82.0                             |
| 21 | offensive_rebounds              | double    | Yes      | Offensive rebounds per 36 minutes                                                |             | 1.8                              |
| 22 | defensive_rebounds              | double    | Yes      | Defensive rebounds per 36 minutes                                                |             | 5.6                              |
| 23 | total_rebounds                  | double    | Yes      | Total rebounds per 36 minutes                                                    |             | 7.4                              |
| 24 | assists                         | double    | Yes      | Assists per 36 minutes                                                           |             | 6.8                              |
| 25 | steals                          | double    | Yes      | Steals per 36 minutes                                                            |             | 1.3                              |
| 26 | blocks                          | double    | Yes      | Blocks per 36 minutes                                                            |             | 0.9                              |
| 27 | turnovers                       | double    | Yes      | Turnovers per 36 minutes                                                         |             | 3.5                              |
| 28 | personal_fouls                  | double    | Yes      | Personal fouls per 36 minutes                                                    |             | 2.4                              |
| 29 | points                          | double    | Yes      | Points scored per 36 minutes                                                     |             | 24.3                             |
