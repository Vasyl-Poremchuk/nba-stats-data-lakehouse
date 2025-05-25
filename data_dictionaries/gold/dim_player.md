## Data Dictionary: `dim_player` table.

| #  | column_name        | data_type | nullable | description                                               | constraints | example                                                                             |
|----|--------------------|-----------|----------|-----------------------------------------------------------|-------------|-------------------------------------------------------------------------------------|
| 1  | player_sk          | string    | No       | Surrogate key generated using MD5 hash of the player name | PK          | 59c526366309f265963b8f6c801e2fb7                                                    |
| 2  | player             | string    | No       | Full name of the basketball player                        |             | Chris Garner                                                                        |
| 3  | shooting_hand      | string    | Yes      | Player's dominant shooting hand                           |             | right                                                                               |
| 4  | high_schools       | string    | Yes      | Semicolon-separated list of high schools attended         |             | Jamesville-DeWitt in DeWitt, New York; Brewster Academy in Wolfeboro, New Hampshire |
| 5  | picked_team        | string    | Yes      | Name of the team that picked the player in the NBA draft  |             | Portland Trail Blazers                                                              |
| 6  | draft_round        | bigint    | Yes      | Draft round in which the player was selected              |             | 2                                                                                   |
| 7  | draft_pick         | bigint    | Yes      | Pick number within the draft round                        |             | 4                                                                                   |
| 8  | overall_draft_pick | bigint    | Yes      | Player's overall pick number in the NBA draft             |             | 34                                                                                  |
| 9  | draft_year         | bigint    | Yes      | Year the player was drafted                               |             | 2021                                                                                |
| 10 | nba_debut          | date      | Yes      | Date of player's first NBA game                           |             | 2021-10-20                                                                          |
