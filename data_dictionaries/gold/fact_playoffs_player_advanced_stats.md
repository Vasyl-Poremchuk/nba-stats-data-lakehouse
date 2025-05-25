## Data Dictionary: `fact_playoffs_player_advanced_stats` table.


| #  | column_name                  | data_type | nullable | description                                                                      | constraints | example                          |
|----|------------------------------|-----------|----------|----------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                    | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)           | FK          | 0c1b198624c9263cdc946d02e83e4a24 |
| 2  | team_sk                      | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)  | FK          | 5452e84700b026429276de4e8e6931df |
| 3  | player_sk                    | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`) | FK          | f3a5c81e37b42f109e09b0d123456789 |
| 4  | rank                         | int       | No       | Player’s rank by advanced playoff performance                                    |             | 5                                |
| 5  | games                        | int       | No       | Number of playoff games played                                                   |             | 18                               |
| 6  | games_started                | int       | No       | Number of playoff games started                                                  |             | 18                               |
| 7  | minutes_played               | int       | No       | Total minutes played in playoffs                                                 |             | 690                              |
| 8  | player_efficiency_rating     | double    | Yes      | Player Efficiency Rating (PER) in playoffs                                       |             | 22.7                             |
| 9  | true_shooting_percentage     | double    | Yes      | True shooting percentage (efficiency metric including FTs and 3PTs)              |             | 57.8                             |
| 10 | 3_point_attempt_rate         | double    | Yes      | Rate of 3-point attempts relative to total field goal attempts                   |             | 0.32                             |
| 11 | free_throw_attempt_rate      | double    | Yes      | Rate of free throw attempts relative to field goal attempts                      |             | 0.28                             |
| 12 | offensive_rebound_percentage | double    | Yes      | Percentage of available offensive rebounds grabbed                               |             | 8.1                              |
| 13 | defensive_rebound_percentage | double    | Yes      | Percentage of available defensive rebounds grabbed                               |             | 18.4                             |
| 14 | total_rebound_percentage     | double    | Yes      | Percentage of available total rebounds grabbed                                   |             | 13.2                             |
| 15 | assist_percentage            | double    | Yes      | Percentage of teammate field goals assisted by the player                        |             | 23.5                             |
| 16 | steal_percentage             | double    | Yes      | Percentage of opponent possessions ending in a steal by the player               |             | 2.4                              |
| 17 | block_percentage             | double    | Yes      | Percentage of opponent shots blocked by the player                               |             | 3.1                              |
| 18 | turnovers_percentage         | double    | Yes      | Percentage of player possessions ending in a turnover                            |             | 12.0                             |
| 19 | usage_percentage             | double    | Yes      | Percentage of team plays used by the player while on the floor                   |             | 30.5                             |
| 20 | offensive_win_shares         | double    | No       | Estimated number of wins contributed by the player’s offense                     |             | 1.8                              |
| 21 | defensive_win_shares         | double    | No       | Estimated number of wins contributed by the player’s defense                     |             | 1.2                              |
| 22 | win_shares                   | double    | No       | Total estimated wins contributed by the player                                   |             | 3.0                              |
| 23 | win_shares_per_48_minutes    | double    | Yes      | Win shares per 48 minutes played                                                 |             | 0.15                             |
| 24 | offensive_box_plus_minus     | double    | Yes      | Offensive Box Plus/Minus (OBPM)                                                  |             | 3.2                              |
| 25 | defensive_box_plus_minus     | double    | Yes      | Defensive Box Plus/Minus (DBPM)                                                  |             | 1.5                              |
| 26 | box_plux_minus               | double    | Yes      | Box Plus/Minus (BPM), combined offensive and defensive impact                    |             | 4.7                              |
| 27 | value_over_replacement       | double    | Yes      | Value Over Replacement Player (VORP)                                             |             | 2.3                              |

