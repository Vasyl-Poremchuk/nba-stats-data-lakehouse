## Data Dictionary: `fact_opponent_total_stats` table.

| #  | column_name                   | data_type | nullable | description                                                                     | constraints | example                          |
|----|-------------------------------|-----------|----------|---------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                     | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)          | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                       | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`) | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | rank                          | string    | No       | Final team ranking within the season                                            |             | 15                               |
| 4  | games                         | bigint    | No       | Total games played by the opponent team                                         |             | 82                               |
| 5  | minutes_played                | bigint    | Yes      | Total minutes played by all players on the opponent team                        |             | 19680                            |
| 6  | field_goals                   | int       | Yes      | Total number of field goals made by the opponent team                           |             | 2900                             |
| 7  | field_goal_attempts           | int       | Yes      | Total number of field goal attempts by the opponent team                        |             | 6500                             |
| 8  | field_goal_percentage         | int       | Yes      | Percentage of successful field goals by the opponent team                       |             | 44                               |
| 9  | 3_point_field_goals           | int       | Yes      | Total number of 3-point field goals made by the opponent team                   |             | 800                              |
| 10 | 3_point_field_goal_attempts   | int       | Yes      | Total number of 3-point field goal attempts by the opponent team                |             | 2200                             |
| 11 | 3_point_field_goal_percentage | double    | Yes      | Percentage of successful 3-point field goals by the opponent team               |             | 36.4                             |
| 12 | 2_point_field_goals           | int       | Yes      | Total number of 2-point field goals made by the opponent team                   |             | 2100                             |
| 13 | 2_point_field_goal_attempts   | int       | Yes      | Total number of 2-point field goal attempts by the opponent team                |             | 4300                             |
| 14 | 2_point_field_goal_percentage | double    | Yes      | Percentage of successful 2-point field goals by the opponent team               |             | 48.8                             |
| 15 | free_throws                   | int       | Yes      | Total number of free throws made by the opponent team                           |             | 700                              |
| 16 | free_throw_attempts           | int       | Yes      | Total number of free throw attempts by the opponent team                        |             | 900                              |
| 17 | free_throw_percentage         | double    | Yes      | Percentage of successful free throws by the opponent team                       |             | 77.8                             |
| 18 | offensive_rebounds            | int       | Yes      | Total number of offensive rebounds collected by the opponent team               |             | 700                              |
| 19 | defensive_rebounds            | int       | Yes      | Total number of defensive rebounds collected by the opponent team               |             | 2200                             |
| 20 | total_rebounds                | int       | Yes      | Total number of rebounds (offensive + defensive) by the opponent team           |             | 2900                             |
| 21 | assists                       | int       | Yes      | Total number of assists made by the opponent team                               |             | 1800                             |
| 22 | steals                        | int       | Yes      | Total number of steals by the opponent team                                     |             | 600                              |
| 23 | blocks                        | int       | Yes      | Total number of blocked shots by the opponent team                              |             | 450                              |
| 24 | turnovers                     | int       | Yes      | Total number of turnovers committed by the opponent team                        |             | 900                              |
| 25 | personal_fouls                | int       | Yes      | Total number of personal fouls committed by the opponent team                   |             | 1600                             |
| 26 | points                        | int       | No       | Total number of points scored by the opponent team                              |             | 9300                             |
| 27 | is_playoff_team               | boolean   | No       | Indicates whether the opponent team made the playoffs                           |             | false                            |
