## Data Dictionary: `fact_regular_season_player_adjusted_shooting_stats` table.

| #  | column_name                         | data_type | nullable | description                                                                           | constraints | example                          |
|----|-------------------------------------|-----------|----------|---------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                           | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)                | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                             | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)       | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                           | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`)      | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                                | int       | No       | Final player ranking within the team based on adjusted shooting performance           |             | 5                                |
| 5  | games                               | int       | No       | Total number of regular season games the player participated in                       |             | 82                               |
| 6  | games_started                       | int       | Yes      | Total number of regular season games the player started                               |             | 82                               |
| 7  | minutes_played                      | int       | No       | Total minutes played by the player during the regular season                          |             | 2900                             |
| 8  | field_goal_percentage               | double    | Yes      | Percentage of all field goal attempts made                                            |             | 47.2                             |
| 9  | 2_point_field_goal_percentage       | double    | Yes      | Percentage of made 2-point field goals                                                |             | 54.1                             |
| 10 | 3_point_field_goal_percentage       | double    | Yes      | Percentage of made 3-point field goals                                                |             | 38.5                             |
| 11 | effective_field_goal_percentage     | double    | Yes      | Adjusted field goal percentage accounting for the added value of 3-point shots        |             | 52.8                             |
| 12 | free_throw_percentage               | double    | Yes      | Percentage of made free throws                                                        |             | 85.3                             |
| 13 | true_shooting_percentage            | double    | Yes      | Shooting efficiency metric that accounts for field goals, 3-pointers, and free throws |             | 58.7                             |
| 14 | free_throw_attempt_rate             | double    | Yes      | Ratio of free throw attempts to field goal attempts                                   |             | 0.25                             |
| 15 | 3_point_attempt_rate                | double    | Yes      | Ratio of 3-point field goal attempts to total field goal attempts                     |             | 0.35                             |
| 16 | adjusted_field_goal                 | int       | Yes      | Adjusted number of field goals made, incorporating weights for different shot types   |             | 180                              |
| 17 | adjusted_2_point_field_goal         | int       | Yes      | Adjusted number of 2-point field goals made                                           |             | 130                              |
| 18 | adjusted_effective_field_goal       | int       | Yes      | Adjusted effective field goals made, accounting for 3-point shot values               |             | 200                              |
| 19 | adjusted_free_throw                 | int       | Yes      | Adjusted number of free throws made                                                   |             | 90                               |
| 20 | adjusted_true_shooting              | int       | Yes      | Adjusted true shooting metric value                                                   |             | 210                              |
| 21 | adjusted_free_throw_attempt         | int       | Yes      | Adjusted number of free throw attempts                                                |             | 110                              |
| 22 | adjusted_3_point_attempt            | int       | Yes      | Adjusted number of 3-point attempts                                                   |             | 130                              |
| 23 | points_added_by_field_goal_shooting | double    | No       | Estimated points contributed by field goal shooting relative to league average        |             | 50.3                             |
| 24 | points_added_by_overall_shooting    | double    | No       | Estimated points contributed by overall shooting performance including free throws    |             | 65.1                             |
