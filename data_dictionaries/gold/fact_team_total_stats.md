## Data Dictionary: `fact_team_total_stats` table.

| #  | column_name                   | data_type | nullable | description                                                                     | constraints | example                          |
|----|-------------------------------|-----------|----------|---------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                     | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)          | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                       | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`) | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | rank                          | string    | No       | Final team ranking within the season                                            |             | 1                                |
| 4  | games                         | bigint    | No       | Total games played by the team                                                  |             | 82                               |
| 5  | minutes_played                | bigint    | No       | Total number of minutes played by all players on the team                       |             | 19788                            |
| 6  | field_goals                   | int       | No       | Total number of field goals made by the team                                    |             | 2707                             |
| 7  | field_goal_attempts           | int       | No       | Total number of field goal attempts by the team                                 |             | 6344                             |
| 8  | field_goal_percentage         | int       | No       | Percentage of field goals made                                                  |             | 43                               |
| 9  | 3_point_field_goals           | int       | Yes      | Total number of 3-point field goals made                                        |             | 320                              |
| 10 | 3_point_field_goal_attempts   | int       | Yes      | Total number of 3-point field goal attempts                                     |             | 890                              |
| 11 | 3_point_field_goal_percentage | double    | Yes      | Percentage of 3-point field goals made                                          |             | 36.0                             |
| 12 | 2_point_field_goals           | int       | No       | Total number of 2-point field goals made                                        |             | 2387                             |
| 13 | 2_point_field_goal_attempts   | int       | No       | Total number of 2-point field goal attempts                                     |             | 5454                             |
| 14 | 2_point_field_goal_percentage | double    | No       | Percentage of 2-point field goals made                                          |             | 44.0                             |
| 15 | free_throws                   | int       | No       | Total number of free throws made                                                |             | 1510                             |
| 16 | free_throw_attempts           | int       | No       | Total number of free throw attempts                                             |             | 1980                             |
| 17 | free_throw_percentage         | double    | No       | Percentage of free throws made                                                  |             | 76.3                             |
| 18 | offensive_rebounds            | int       | Yes      | Total number of offensive rebounds collected                                    |             | 880                              |
| 19 | defensive_rebounds            | int       | Yes      | Total number of defensive rebounds collected                                    |             | 2370                             |
| 20 | total_rebounds                | int       | No       | Total number of rebounds (offensive + defensive)                                |             | 3250                             |
| 21 | assists                       | int       | No       | Total number of assists made by the team                                        |             | 1340                             |
| 22 | steals                        | int       | Yes      | Total number of steals by the team                                              |             | 520                              |
| 23 | blocks                        | int       | Yes      | Total number of blocked shots by the team                                       |             | 390                              |
| 24 | turnovers                     | int       | Yes      | Total number of turnovers committed by the team                                 |             | 880                              |
| 25 | personal_fouls                | int       | No       | Total number of personal fouls committed by the team                            |             | 1280                             |
| 26 | points                        | int       | No       | Total number of points scored by the team                                       |             | 6400                             |
| 27 | is_playoff_team               | boolean   | No       | Indicates whether the team made the playoffs                                    |             | false                            |
