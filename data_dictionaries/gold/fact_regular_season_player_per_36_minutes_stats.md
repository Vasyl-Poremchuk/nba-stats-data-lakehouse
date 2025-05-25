## Data Dictionary: `fact_regular_season_player_per_36_minutes_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                               | constraints | example                          |
|----|---------------------------------|-----------|----------|-------------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)                    | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)           | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`)          | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                            | int       | No       | Ranking of the player within the team or season based on performance                      |             | 2                                |
| 5  | games                           | int       | No       | Number of games played in the season                                                      |             | 75                               |
| 6  | games_started                   | int       | Yes      | Number of games started in the season                                                     |             | 75                               |
| 7  | minutes_played                  | int       | No       | Total minutes played in the season                                                        |             | 2700                             |
| 8  | field_goals                     | double    | Yes      | Average field goals made per 36 minutes                                                   |             | 8.5                              |
| 9  | field_goal_attempts             | double    | Yes      | Average field goal attempts per 36 minutes                                                |             | 17.2                             |
| 10 | field_goal_percentage           | double    | Yes      | Field goal shooting percentage per 36 minutes                                             |             | 49.4                             |
| 11 | 3_point_field_goals             | double    | Yes      | Average 3-point field goals made per 36 minutes                                           |             | 3.1                              |
| 12 | 3_point_field_goal_attempts     | double    | Yes      | Average 3-point field goal attempts per 36 minutes                                        |             | 7.5                              |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | 3-point field goal shooting percentage per 36 minutes                                     |             | 41.3                             |
| 14 | 2_point_field_goals             | double    | Yes      | Average 2-point field goals made per 36 minutes                                           |             | 5.4                              |
| 15 | 2_point_field_goal_attempts     | double    | Yes      | Average 2-point field goal attempts per 36 minutes                                        |             | 9.7                              |
| 16 | 2_point_field_goal_percentage   | double    | Yes      | 2-point field goal shooting percentage per 36 minutes                                     |             | 55.7                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage per 36 minutes (accounts for 3-pointers being worth more) |             | 56.1                             |
| 18 | free_throws                     | double    | Yes      | Average free throws made per 36 minutes                                                   |             | 6.2                              |
| 19 | free_throw_attempts             | double    | Yes      | Average free throw attempts per 36 minutes                                                |             | 7.3                              |
| 20 | free_throw_percentage           | double    | Yes      | Free throw shooting percentage per 36 minutes                                             |             | 84.9                             |
| 21 | offensive_rebounds              | double    | Yes      | Average offensive rebounds per 36 minutes                                                 |             | 1.4                              |
| 22 | defensive_rebounds              | double    | Yes      | Average defensive rebounds per 36 minutes                                                 |             | 4.8                              |
| 23 | total_rebounds                  | double    | Yes      | Average total rebounds per 36 minutes                                                     |             | 6.2                              |
| 24 | assists                         | double    | Yes      | Average assists per 36 minutes                                                            |             | 7.1                              |
| 25 | steals                          | double    | Yes      | Average steals per 36 minutes                                                             |             | 1.8                              |
| 26 | blocks                          | double    | Yes      | Average blocks per 36 minutes                                                             |             | 0.6                              |
| 27 | turnovers                       | double    | Yes      | Average turnovers per 36 minutes                                                          |             | 2.5                              |
| 28 | personal_fouls                  | double    | Yes      | Average personal fouls per 36 minutes                                                     |             | 2.1                              |
| 29 | points                          | double    | Yes      | Average points scored per 36 minutes                                                      |             | 26.3                             |
