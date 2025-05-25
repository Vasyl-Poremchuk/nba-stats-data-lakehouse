## Data Dictionary: `fact_regular_season_player_advanced_stats` table.

| #  | column_name                   | data_type | nullable | description                                                                          | constraints | example                          |
|----|-------------------------------|-----------|----------|--------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                     | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)               | FK          | 60a03b5878a3e5aadf15db0b7607b930 |
| 2  | team_sk                       | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)      | FK          | e938c5bbd29de26c3a600a0330465f8b |
| 3  | player_sk                     | string    | No       | Surrogate key generated using MD5 hash of the player name (e.g., `LeBron James`)     | FK          | 8b1a9953c4611296a827abf8c47804d7 |
| 4  | rank                          | int       | No       | Final player ranking within the team based on advanced stats performance             |             | 3                                |
| 5  | games                         | int       | No       | Total number of regular season games the player participated in                      |             | 82                               |
| 6  | games_started                 | int       | Yes      | Total number of regular season games the player started                              |             | 82                               |
| 7  | minutes_played                | int       | No       | Total minutes played by the player during the regular season                         |             | 2800                             |
| 8  | player_efficiency_rating      | double    | Yes      | A measure of a player's overall statistical performance                              |             | 24.5                             |
| 9  | true_shooting_percentage      | double    | Yes      | Shooting efficiency metric accounting for field goals, 3-pointers, and free throws   |             | 58.2                             |
| 10 | 3_point_attempt_rate          | double    | Yes      | Ratio of 3-point field goal attempts to total field goal attempts                    |             | 0.33                             |
| 11 | free_throw_attempt_rate       | double    | Yes      | Ratio of free throw attempts to field goal attempts                                  |             | 0.22                             |
| 12 | offensive_rebound_percentage  | double    | No       | Percentage of available offensive rebounds secured by the player                     |             | 6.1                              |
| 13 | defensive_rebound_percentage  | double    | No       | Percentage of available defensive rebounds secured by the player                     |             | 12.4                             |
| 14 | total_rebound_percentage      | double    | Yes      | Percentage of total available rebounds secured by the player                         |             | 9.3                              |
| 15 | assist_percentage             | double    | Yes      | Percentage of teammate field goals assisted by the player                            |             | 20.5                             |
| 16 | steal_percentage              | double    | Yes      | Percentage of opponent possessions that end with a steal by the player               |             | 2.3                              |
| 17 | block_percentage              | double    | Yes      | Percentage of opponent two-point field goal attempts blocked by the player           |             | 3.8                              |
| 18 | turnovers_percentage          | double    | Yes      | Percentage of player possessions ending in a turnover                                |             | 12.1                             |
| 19 | usage_percentage              | double    | Yes      | Percentage of team plays used by the player while on the floor                       |             | 28.0                             |
| 20 | offensive_win_shares          | double    | Yes      | Estimate of wins contributed by the player due to offensive performance              |             | 5.2                              |
| 21 | defensive_win_shares          | double    | Yes      | Estimate of wins contributed by the player due to defensive performance              |             | 3.4                              |
| 22 | win_shares                    | double    | No       | Total estimate of wins contributed by the player                                     |             | 8.6                              |
| 23 | win_shares_per_48_minutes     | double    | Yes      | Estimate of wins contributed per 48 minutes of play                                  |             | 0.20                             |
| 24 | offensive_box_plus_minus      | double    | Yes      | Estimate of offensive points contributed above average per 100 offensive possessions |             | 3.5                              |
| 25 | defensive_box_plus_minus      | double    | Yes      | Estimate of defensive points contributed above average per 100 defensive possessions |             | 1.8                              |
| 26 | box_plus_minus                | double    | Yes      | Net points contributed per 100 possessions (offensive plus defensive)                |             | 5.3                              |
| 27 | value_over_replacement_player | double    | Yes      | Estimate of player's overall value above a replacement-level player                  |             | 4.0                              |

