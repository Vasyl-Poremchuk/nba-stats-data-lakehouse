## Data Dictionary: `fact_team_per_100_possessions_stats` table.

| #  | column_name                   | data_type | nullable | description                                                                     | constraints | example                          |
|----|-------------------------------|-----------|----------|---------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                     | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)          | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                       | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`) | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | rank                          | bigint    | No       | Final team ranking within the season                                            |             | 1                                |
| 4  | games                         | bigint    | No       | Total games played by the team                                                  |             | 82                               |
| 5  | minutes_played                | bigint    | No       | Total number of minutes played by all players on the team                       |             | 241.5                            |
| 6  | field_goals                   | double    | No       | Average number of field goals made by the team per 100 possessions              |             | 33.1                             |
| 7  | field_goal_attempts           | double    | No       | Average number of field goal attempts by the team per 100 possessions           |             | 77.5                             |
| 8  | field_goal_percentage         | double    | No       | Percentage of field goals made                                                  |             | 42.6                             |
| 9  | 3_point_field_goals           | double    | Yes      | Average number of 3-point field goals made per 100 possessions                  |             | 3.9                              |
| 10 | 3_point_field_goal_attempts   | double    | Yes      | Average number of 3-point field goal attempts per 100 possessions               |             | 10.7                             |
| 11 | 3_point_field_goal_percentage | double    | Yes      | Percentage of 3-point field goals made                                          |             | 36.7                             |
| 12 | 2_point_field_goals           | double    | No       | Average number of 2-point field goals made per 100 possessions                  |             | 29.1                             |
| 13 | 2_point_field_goal_attempts   | double    | No       | Average number of 2-point field goal attempts per 100 possessions               |             | 66.8                             |
| 14 | 2_point_field_goal_percentage | double    | No       | Percentage of 2-point field goals made                                          |             | 43.6                             |
| 15 | free_throws                   | double    | No       | Average number of free throws made per 100 possessions                          |             | 18.3                             |
| 16 | free_throw_attempts           | double    | No       | Average number of free throw attempts per 100 possessions                       |             | 23.8                             |
| 17 | free_throw_percentage         | double    | No       | Percentage of free throws made                                                  |             | 76.8                             |
| 18 | offensive_rebounds            | double    | No       | Average number of offensive rebounds collected per 100 possessions              |             | 10.9                             |
| 19 | defensive_rebounds            | double    | No       | Average number of defensive rebounds collected per 100 possessions              |             | 29.3                             |
| 20 | total_rebounds                | double    | No       | Average number of total rebounds (offensive + defensive) per 100 possessions    |             | 40.2                             |
| 21 | assists                       | double    | No       | Average number of assists made by the team per 100 possessions                  |             | 16.9                             |
| 22 | steals                        | double    | No       | Average number of steals by the team per 100 possessions                        |             | 7.2                              |
| 23 | blocks                        | double    | No       | Average number of blocked shots by the team per 100 possessions                 |             | 5.1                              |
| 24 | turnovers                     | double    | No       | Average number of turnovers committed by the team per 100 possessions           |             | 15.1                             |
| 25 | personal_fouls                | double    | No       | Average number of personal fouls committed by the team per 100 possessions      |             | 23.1                             |
| 26 | points                        | double    | No       | Average number of points scored by the team per 100 possessions                 |             | 88.4                             |
| 27 | is_playoff_team               | boolean   | No       | Indicates whether the team made the playoffs                                    |             | false                            |
