## Data Dictionary: `fact_playoffs_player_total_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                      | constraints | example                          |
|----|---------------------------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                            | int       | No       | Final player ranking within the team based on overall playoff performance        |             | 3                                |
| 5  | games                           | int       | No       | Total number of playoff games the player participated in                         |             | 20                               |
| 6  | games_started                   | int       | No       | Total number of playoff games the player started                                 |             | 20                               |
| 7  | minutes_played                  | int       | No       | Total minutes played by the player during the playoffs                           |             | 750                              |
| 8  | field_goals                     | int       | No       | Total number of field goals made                                                 |             | 180                              |
| 9  | field_goal_attempts             | int       | No       | Total number of field goal attempts                                              |             | 375                              |
| 10 | field_goal_percentage           | double    | Yes      | Percentage of made field goals                                                   |             | 375                              |
| 11 | 3_point_field_goals             | int       | Yes      | Total number of successful 3-point field goals                                   |             | 50                               |
| 12 | 3_point_field_goal_attempts     | int       | Yes      | Total number of 3-point field goal attempts                                      |             | 130                              |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | Percentage of made 3-point field goals                                           |             | 38.5                             |
| 14 | 2_point_field_goals             | int       | Yes      | Total number of successful 2-point field goals                                   |             | 130                              |
| 15 | 2_point_field_goal_attempts     | int       | Yes      | Total number of 2-point field goal attempts                                      |             | 245                              |
| 16 | 2_point_field_goal_percentage   | double    | Yes      | Percentage of made 2-point field goals                                           |             | 53.1                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Adjusted field goal percentage that accounts for 3-point shots                   |             | 54.2                             |
| 18 | free_throws                     | int       | Yes      | Total number of free throws made                                                 |             | 90                               |
| 19 | free_throw_attempts             | int       | Yes      | Total number of free throw attempts                                              |             | 110                              |
| 20 | free_throw_percentage           | double    | Yes      | Percentage of made free throws                                                   |             | 81.8                             |
| 21 | offensive_rebounds              | int       | Yes      | Total number of offensive rebounds                                               |             | 40                               |
| 22 | defensive_rebounds              | int       | Yes      | Total number of defensive rebounds                                               |             | 110                              |
| 23 | total_rebounds                  | int       | No       | Total number of rebounds (offensive + defensive)                                 |             | 150                              |
| 24 | assists                         | int       | No       | Total number of assists                                                          |             | 60                               |
| 25 | steals                          | int       | Yes      | Total number of steals                                                           |             | 25                               |
| 26 | blocks                          | int       | Yes      | Total number of blocks                                                           |             | 15                               |
| 27 | turnovers                       | int       | Yes      | Total number of turnovers                                                        |             | 30                               |
| 28 | personal_fouls                  | int       | No       | Total number of personal fouls                                                   |             | 22                               |
| 29 | points                          | int       | No       | Total number of points scored                                                    |             | 500                              |
| 30 | triple_doubles                  | int       | No       | Number of triple-double performances during the playoffs                         |             | 1                                |
