## Data Dictionary: `dim_roster` table.

| #  | column_name           | data_type | nullable | description                                                                | constraints                  | example                          |
|----|-----------------------|-----------|----------|----------------------------------------------------------------------------|------------------------------|----------------------------------|
| 1  | season_sk             | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)     | PK (part of a composite key) | e223ce6af98e663849c50b62d9b6b4cc |
| 2  | team_sk               | string    | No       | Surrogate key generated using MD5 hash of the team (e.g., `Chicago Bulls`) | PK (part of a composite key) | e40ac1523f13aca7f78b5f3b421c37a0 |
| 3  | player_sk             | string    | No       | Surrogate key generated using MD5 hash of the player name                  | PK (part of a composite key) | 63a51559b5041a9f653e144f79589512 |
| 4  | player                | string    | No       | Full name of the player                                                    |                              | Darrell Armstrong                |
| 5  | uniform_number        | string    | No       | Player's jersey number during the season                                   |                              | 10                               |
| 6  | position              | string    | No       | Player's on-court position                                                 |                              | PG                               |
| 7  | height                | string    | No       | Player's height (e.g., in feet/inches)                                     |                              | 6-0                              |
| 8  | weight                | bigint    | No       | Player's weight in pounds                                                  |                              | 170                              |
| 9  | birth_date            | date      | No       | Player's date of birth                                                     |                              | 1968-06-22                       |
| 10 | country_of_birth      | string    | No       | Country where the player was born                                          |                              | US                               |
| 11 | years_experience      | string    | No       | Number of years the player has played in the NBA                           |                              | 11                               |
| 12 | college               | string    | Yes      | College the player attended                                                |                              | Fayetteville State University    |
| 13 | regular_season_awards | string    | No       | Comma-separated list of regular season awards received                     |                              | No Awards                        |
| 14 | playoffs_awards       | string    | No       | Comma-separated list of playoffs awards received                           |                              | No Awards                        |
