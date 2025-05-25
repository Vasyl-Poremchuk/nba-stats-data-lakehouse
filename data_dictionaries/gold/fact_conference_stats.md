## Data Dictionary: `fact_conference_stats` table.

| #  | column_name              | data_type | nullable | description                                                                          | constraints | example                          |
|----|--------------------------|-----------|----------|--------------------------------------------------------------------------------------|-------------|----------------------------------|
| 1  | season_sk                | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)               | FK          | 0a19f101b49d5e2816d7568fc29280e9 |
| 2  | conference_sk            | string    | No       | Surrogate key generated using MD5 hash of the conference (e.g., `Eastern`)           | FK          | 988c64336b8b535611fc1f617eca2cef |
| 3  | division_sk              | string    | No       | Surrogate key generated using MD5 hash of the division (e.g., `Atlantic`)            | FK          | f17af17f6b59b4e7f1d4a6e99fbf7675 |
| 4  | team_sk                  | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`)      | FK          | fba924f8a9dee09aa85b56e258506f9c |
| 5  | wins                     | bigint    | No       | Total number of regular season games won by the team                                 |             | 59                               |
| 6  | losses                   | bigint    | No       | Total number of regular season games lost by the team                                |             | 23                               |
| 7  | wins_loss_percentage     | double    | No       | Win ratio over the season: wins / (wins + losses)                                    |             | 0.72                             |
| 8  | games_behind             | bigint    | No       | Number of games behind the top team in the division or conference standings          |             | 0                                |
| 9  | points_per_game          | double    | No       | Average number of points scored by the team per game                                 |             | 111.7                            |
| 10 | opponent_points_per_game | double    | No       | Average number f points allowed per game by the team                                 |             | 103.9                            |
| 11 | simple_rating_system     | double    | No       | A rating that takes into account average point differential and strength of schedule |             | 7.29                             |
| 12 | is_playoff_team          | boolean   | No       | Indicates whether the team qualified for the playoffs                                |             | true                             |
