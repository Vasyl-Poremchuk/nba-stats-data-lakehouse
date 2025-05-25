## Data Dictionary: `fact_playoffs_player_per_game_stats` table.

| #  | column_name                     | data_type | nullable | description                                               | constraints | example                          |
|----|---------------------------------|-----------|----------|-----------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                       | string    | No       | Surrogate key for the season (e.g., `2023-24`)            | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                         | string    | No       | Surrogate key for the team (e.g., `Chicago Bulls`)        | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                       | string    | No       | Surrogate key for the player (e.g., `LeBron James`)       | FK          | 78a03b58a123e5aa1f1db0b5a607b931 |
| 4  | rank                            | int       | No       | Player rank within the team or league for the season      |             | 3                                |
| 5  | games                           | int       | No       | Number of playoff games the player appeared in            |             | 15                               |
| 6  | games_started                   | int       | Yes      | Number of playoff games the player started                |             | 15                               |
| 7  | minutes_played                  | double    | No       | Average minutes played per game in playoffs               |             | 34.5                             |
| 8  | field_goals                     | double    | No       | Average field goals made per game                         |             | 8.2                              |
| 9  | field_goal_attempts             | double    | No       | Average field goal attempts per game                      |             | 18.1                             |
| 10 | field_goal_percentage           | double    | Yes      | Field goal shooting percentage                            |             | 45.3                             |
| 11 | 3_point_field_goals             | double    | Yes      | Average 3-point field goals made per game                 |             | 2.1                              |
| 12 | 3_point_field_goal_attempts     | double    | Yes      | Average 3-point field goal attempts per game              |             | 5.7                              |
| 13 | 3_point_field_goal_percentage   | double    | Yes      | 3-point shooting percentage                               |             | 36.8                             |
| 14 | 2_point_field_goals             | double    | Yes      | Average 2-point field goals made per game                 |             | 6.1                              |
| 15 | 2_point_field_goal_attempts     | double    | Yes      | Average 2-point field goal attempts per game              |             | 12.4                             |
| 16 | 2_point_field_goal_percentage   | double    | Yes      | 2-point shooting percentage                               |             | 49.2                             |
| 17 | effective_field_goal_percentage | double    | Yes      | Effective field goal percentage (adjusted for 3-pointers) |             | 53.1                             |
| 18 | free_throws                     | double    | No       | Average free throws made per game                         |             | 5.3                              |
| 19 | free_throw_attempts             | double    | No       | Average free throw attempts per game                      |             | 6.0                              |
| 20 | free_throw_percentage           | double    | Yes      | Free throw shooting percentage                            |             | 88.3                             |
| 21 | offensive_rebounds              | double    | Yes      | Average offensive rebounds per game                       |             | 1.2                              |
| 22 | defensive_rebounds              | double    | Yes      | Average defensive rebounds per game                       |             | 5.4                              |
| 23 | total_rebounds                  | double    | Yes      | Average total rebounds per game                           |             | 6.6                              |
| 24 | assists                         | double    | No       | Average assists per game                                  |             | 7.8                              |
| 25 | steals                          | double    | Yes      | Average steals per game                                   |             | 1.5                              |
| 26 | blocks                          | double    | Yes      | Average blocks per game                                   |             | 0.9                              |
| 27 | turnovers                       | double    | Yes      | Average turnovers per game                                |             | 3.2                              |
| 28 | personal_fouls                  | double    | No       | Average personal fouls per game                           |             | 2.4                              |
| 29 | points                          | double    | Yes      | Average points scored per game                            |             | 23.8                             |
