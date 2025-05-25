| #  | column_name                   | data_type | nullable | description                                                                     | constraints | example                          |
|----|-------------------------------|-----------|----------|---------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                     | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)          | FK          | 0c1b198624c9263cdc946d02e83e4a24 |
| 2  | team_sk                       | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`) | FK          | 5452e84700b026429276de4e8e6931df |
| 3  | rank                          | bigint    | No       | Final team ranking withing the season                                           |             | 1                                |
| 4  | games                         | bigint    | No       | Total games played by the team                                                  |             | 82                               |
| 5  | minutes_played                | bigint    | No       | Average number of  minutes played by all players on the team                    |             | 19755                            |
| 6  | field_goals                   | double    | No       | Average number of field goals made by the team                                  |             | 36.3                             |
| 7  | field_goal_attempts           | double    | No       | Average number of field goal attempts by the team                               |             | 84.4                             |
| 8  | field_goal_percentage         | double    | No       | Percentage of field goals made                                                  |             | 43.1                             |
| 9  | 3_point_field_goals           | double    | Yes      | Average number of 3-point field goals made                                      |             | 3.3                              |
| 10 | 3_point_field_goal_attempts   | double    | Yes      | Average number of 3-point field goal attempts                                   |             | 10.8                             |
| 11 | 3_point_field_goal_percentage | double    | Yes      | Percentage of 3-point field goals made                                          |             | 30.7                             |
| 12 | 2_point_field_goals           | double    | No       | Average number of 2-point field goals made                                      |             | 33.1                             |
| 13 | 2_point_field_goal_attempts   | double    | No       | Average number of 2-point field goal attempts                                   |             | 73.6                             |
| 14 | 2_point_field_goal_percentage | double    | No       | Percentage of 2-point field goals made                                          |             | 45.0                             |
| 15 | free_throws                   | double    | No       | Average number of free throws made                                              |             | 22.0                             |
| 16 | free_throw_attempts           | double    | No       | Average number of free throw attempts                                           |             | 30.6                             |
| 17 | free_throw_percentage         | double    | No       | Percentage of free throws made                                                  |             | 71.9                             |
| 18 | offensive_rebounds            | double    | No       | Average number of offensive rebounds collected                                  |             | 13.3                             |
| 19 | defensive_rebounds            | double    | No       | Average number of defensive rebounds collected                                  |             | 29.4                             |
| 20 | total_rebounds                | double    | No       | Average number of rebounds (offensive + defensive)                              |             | 42.7                             |
| 21 | assists                       | double    | No       | Average number of assists made by the team                                      |             | 21.9                             |
| 22 | steals                        | double    | No       | Average number of steals by the team                                            |             | 8.9                              |
| 23 | blocks                        | double    | No       | Average number of blocked shots by the team                                     |             | 4.4                              |
| 24 | turnovers                     | double    | No       | Average number of turnovers committed by the team                               |             | 18.6                             |
| 25 | personal_fouls                | double    | No       | Average number of personal fouls committed by the team                          |             | 24.8                             |
| 26 | points                        | double    | No       | Average number of points scored by the team                                     |             | 98.2                             |
| 27 | is_playoff_team               | boolean   | No       | Indicates whether team made the playoffs                                        |             | true                             |

