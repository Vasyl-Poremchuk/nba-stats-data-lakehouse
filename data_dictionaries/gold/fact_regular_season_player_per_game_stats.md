## Data Dictionary: `fact_regular_season_player_per_game_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                      | constraints | example                          |
|----|---------------------------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                            | int       | No       | Player's rank based on performance within the team/league                        |             | 3                                |
| 5  | games                           | int       | No       | Number of games played                                                           |             | 82                               |
| 6  | games_started                   | int       | Yes      | Number of games started                                                          |             | 80                               |
| 7  | minutes_played                  | double    | No       | Total minutes played                                                             |             | 2785.3                           |
| 8  | field_goals                     | double    | No       | Field goals made per game                                                        |             | 7.8                              |
| 9  | field_goal_attempts             | double    | No       | Field goal attempts per game                                                     |             | 17.2                             |
| 10 | field_goal_percentage           | double    | Yes      | Field goal shooting percentage                                                   |             | 45.3                             |
| 11 | 3_point_field_goals             | double    | Yes      | 3-point field goals made per game                                                |             | 2.5                              |
| 12 | 3_point_field_goal_attempts     | double    | Yes      | 3-point field goal attempts per game                                             |             | 6.9                              |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | 3-point field goal shooting percentage                                           |             | 36.2                             |
| 14 | 2_point_field_goals             | double    | Yes      | 2-point field goals made per game                                                |             | 5.3                              |
| 15 | 2_point_field_goal_attempts     | double    | Yes      | 2-point field goal attempts per game                                             |             | 10.3                             |
| 16 | 2_point_field_goal_percentage   | double    | Yes      | 2-point field goal shooting percentage                                           |             | 51.5                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage (accounts for 3-pointers)                        |             | 49.5                             |
| 18 | free_throws                     | double    | No       | Free throws made per game                                                        |             | 4.1                              |
| 19 | free_throw_attempts             | double    | No       | Free throw attempts per game                                                     |             | 5.2                              |
| 20 | free_throw_percentage           | double    | Yes      | Free throw shooting percentage                                                   |             | 79.2                             |
| 21 | offensive_rebounds              | double    | Yes      | Offensive rebounds per game                                                      |             | 0.8                              |
| 22 | defensive_rebounds              | double    | Yes      | Defensive rebounds per game                                                      |             | 4.1                              |
| 23 | total_rebounds                  | double    | No       | Total rebounds per game                                                          |             | 4.9                              |
| 24 | assists                         | double    | No       | Assists per game                                                                 |             | 5.6                              |
| 25 | steals                          | double    | Yes      | Steals per game                                                                  |             | 1.3                              |
| 26 | blocks                          | double    | Yes      | Blocks per game                                                                  |             | 0.7                              |
| 27 | turnovers                       | double    | Yes      | Turnovers per game                                                               |             | 2.5                              |
| 28 | personal_fouls                  | double    | No       | Personal fouls per game                                                          |             | 2.4                              |
| 29 | points                          | double    | Yes      | Points scored per game                                                           |             | 22.2                             |

