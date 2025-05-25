## Data Dictionary: `fact_regular_season_player_per_100_possessions_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                             | constraints | example                          |
|----|---------------------------------|-----------|----------|-----------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)                  | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Golden State Warriors`) | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `Kevin Durant`)        | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                            | int       | No       | Player's rank based on performance within the team or league                            |             | 5                                |
| 5  | games                           | int       | No       | Number of games played during the season                                                |             | 82                               |
| 6  | games_started                   | int       | Yes      | Number of games started                                                                 |             | 80                               |
| 7  | minutes_played                  | int       | No       | Total minutes played                                                                    |             | 2900                             |
| 8  | field_goals                     | double    | Yes      | Field goals made per 100 possessions                                                    |             | 25.3                             |
| 9  | field_goal_attempts             | double    | Yes      | Field goal attempts per 100 possessions                                                 |             | 55.4                             |
| 10 | field_goal_percentage           | double    | Yes      | Field goal percentage per 100 possessions                                               |             | 45.7                             |
| 11 | 3_point_field_goals             | double    | Yes      | 3-point field goals made per 100 possessions                                            |             | 8.6                              |
| 12 | 3_point_field_goal_attempts     | double    | Yes      | 3-point field goal attempts per 100 possessions                                         |             | 23.4                             |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | 3-point field goal shooting percentage per 100 possessions                              |             | 36.8                             |
| 14 | 2_point_field_goals             | double    | Yes      | 2-point field goals made per 100 possessions                                            |             | 16.7                             |
| 15 | 2_point_field_goal_attempts     | double    | Yes      | 2-point field goal attempts per 100 possessions                                         |             | 32.0                             |
| 16 | 2_point_field_goal_percentage   | double    | Yes      | 2-point field goal shooting percentage per 100 possessions                              |             | 52.2                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage per 100 possessions (weights 3PT shots more)            |             | 51.2                             |
| 18 | free_throws                     | double    | Yes      | Free throws made per 100 possessions                                                    |             | 12.4                             |
| 19 | free_throw_attempts             | double    | Yes      | Free throw attempts per 100 possessions                                                 |             | 15.2                             |
| 20 | free_throw_percentage           | double    | Yes      | Free throw shooting percentage per 100 possessions                                      |             | 81.5                             |
| 21 | offensive_rebounds              | double    | Yes      | Offensive rebounds per 100 possessions                                                  |             | 3.2                              |
| 22 | defensive_rebounds              | double    | Yes      | Defensive rebounds per 100 possessions                                                  |             | 9.4                              |
| 23 | total_rebounds                  | double    | Yes      | Total rebounds per 100 possessions                                                      |             | 12.6                             |
| 24 | assists                         | double    | Yes      | Assists per 100 possessions                                                             |             | 18.1                             |
| 25 | steals                          | double    | Yes      | Steals per 100 possessions                                                              |             | 3.5                              |
| 26 | blocks                          | double    | Yes      | Blocks per 100 possessions                                                              |             | 2.2                              |
| 27 | turnovers                       | double    | Yes      | Turnovers per 100 possessions                                                           |             | 5.6                              |
| 28 | personal_fouls                  | double    | Yes      | Personal fouls per 100 possessions                                                      |             | 4.3                              |
| 29 | points                          | double    | Yes      | Points scored per 100 possessions                                                       |             | 65.1                             |
| 30 | offensive_rating                | int       | Yes      | Offensive rating (a measure of offensive efficiency per 100 possessions)                |             | 110                              |
| 31 | defensive_rating                | int       | Yes      | Defensive rating (a measure of defensive efficiency per 100 possessions)                |             | 105                              |

