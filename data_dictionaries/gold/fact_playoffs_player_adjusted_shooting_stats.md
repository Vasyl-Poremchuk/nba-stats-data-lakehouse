## Data Dictionary: `fact_playoffs_player_adjusted_shooting_stats` table.

| #  | column_name                     | data_type | nullable | description                                                                      | constraints | example                          |
|----|---------------------------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 0c1b198624c9263cdc946d02e83e4a24 |
| 2  | team_sk                         | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | 5452e84700b026429276de4e8e6931df |
| 3  | player_sk                       | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | f3a5c81e37b42f109e09b0d123456789 |
| 4  | rank                            | int       | No       | Player’s rank by adjusted shooting efficiency                                    |             | 1                                |
| 5  | games                           | int       | No       | Number of playoff games played                                                   |             | 20                               |
| 6  | games_started                   | int       | No       | Number of playoff games started                                                  |             | 20                               |
| 7  | minutes_played                  | int       | No       | Total minutes played in playoffs                                                 |             | 750                              |
| 8  | field_goal_percentage           | double    | Yes      | Field goal percentage in playoffs                                                |             | 48.5                             |
| 9  | 2_point_field_goal_percentage   | double    | Yes      | 2-point field goal percentage in playoffs                                        |             | 52.1                             |
| 10 | 3_point_field_goal_percentage   | double    | Yes      | 3-point field goal percentage in playoffs                                        |             | 39.7                             |
| 11 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage accounting for 3-point shots                     |             | 55.3                             |
| 12 | free_throw_percentage           | double    | Yes      | Free throw percentage in playoffs                                                |             | 81.2                             |
| 13 | true_shooting_percentage        | double    | Yes      | True shooting percentage (efficiency metric including FTs and 3PTs)              |             | 60.4                             |
| 14 | free_throw_percentage           | double    | Yes      | Duplicate column, same as above (may require cleanup)                            |             | 81.2                             |
| 15 | 3_point_attempt_rate            | double    | Yes      | Rate of 3-point attempts relative to total field goal attempts                   |             | 0.35                             |
| 16 | adjusted_field_goal             | int       | Yes      | Adjusted field goals made                                                        |             | 300                              |
| 17 | adjusted_2_point_field_goal     | int       | Yes      | Adjusted 2-point field goals made                                                |             | 200                              |
| 18 | adjusted_3_point_field_goal     | int       | Yes      | Adjusted 3-point field goals made                                                |             | 100                              |
| 19 | adjusted_effective_field_goal   | int       | Yes      | Adjusted effective field goals                                                   |             | 330                              |
| 20 | adjusted_free_throw             | int       | Yes      | Adjusted free throws made                                                        |             | 180                              |
| 21 | adjusted_true_shooting          | int       | Yes      | Adjusted true shooting metric value                                              |             | 360                              |
| 22 | adjusted_free_throw_attempt     | int       | Yes      | Adjusted free throw attempts                                                     |             | 220                              |
| 23 | adjusted_3_point_attempt        | int       | Yes      | Adjusted 3-point attempts                                                        |             | 280                              |
