## Data Dictionary: `fact_playoffs_player_play_by_play_stats` table

| #  | column_name                             | data_type | nullable | description                                                                          | constraints | example                          |
|----|-----------------------------------------|-----------|----------|--------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                               | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)               | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                                 | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)      | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                               | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`)     | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                                    | int       | No       | Final player ranking within the team based on performance during the playoffs        |             | 1                                |
| 5  | games                                   | int       | No       | Total number of playoff games the player participated in                             |             | 20                               |
| 6  | games_started                           | int       | No       | Total number of playoff games the player started                                     |             | 20                               |
| 7  | minutes_played                          | int       | No       | Total number of minutes played by the player during the playoffs                     |             | 750                              |
| 8  | point_guard_percentage                  | double    | Yes      | Percentage of total minutes the player played at point guard position                |             | 35.5                             |
| 9  | shooting_guard_percentage               | double    | Yes      | Percentage of total minutes the player played at shooting guard position             |             | 40.0                             |
| 10 | small_forward_percentage                | double    | Yes      | Percentage of total minutes the player played at small forward position              |             | 15.0                             |
| 11 | power_forward_percentage                | double    | Yes      | Percentage of total minutes the player played at power forward position              |             | 5.0                              |
| 12 | center_percentage                       | double    | Yes      | Percentage of total minutes the player played at center position                     |             | 4.5                              |
| 13 | plus_minus_per_100_possessions_on_court | double    | Yes      | Team's point differential per 100 possessions while the player was on the court      |             | 8.2                              |
| 14 | plus_minus_net_per_100_possessions      | double    | Yes      | Net point differential per 100 possessions (on court minus off court) for the player |             | 4.5                              |
| 15 | turnovers_by_bad_pass                   | int       | No       | Number of turnovers committed by the player due to bad passes                        |             | 12                               |
| 16 | lost_ball_turnovers                     | int       | No       | Number of turnovers committed by the player due to losing ball control               |             | 8                                |
| 17 | shooting_fouls                          | int       | No       | Number of shooting fouls committed by the player                                     |             | 25                               |
| 18 | offensive_fouls                         | int       | No       | Number of offensive fouls committed by the player                                    |             | 5                                |
| 19 | shooting_fouls_drawn                    | int       | No       | Number of shooting fouls drawn by the player                                         |             | 18                               |
| 20 | offensive_fouls_drawn                   | int       | Yes      | Number of offensive fouls drawn by the player                                        |             | 4                                |
| 21 | point_generated_by_assists              | int       | No       | Total number of points scored by teammates directly off the player's assists         |             | 220                              |
| 22 | fouled_field_goals                      | int       | No       | Number of field goals made by the player while being fouled                          |             | 30                               |
| 23 | blocked_field_goal_attempts             | int       | No       | Number of the player’s field goal attempts that were blocked by the opponent         |             | 10                               |
