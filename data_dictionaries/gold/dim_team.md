## Data Dictionary: `dim_team` table.

| # | column_name | data_type | nullable | description                                             | constraints | example                            |
|---|-------------|-----------|----------|---------------------------------------------------------|-------------|------------------------------------|
| 1 | team_sk     | string    | No       | Surrogate key generated using MD5 hash of the team name | PK          | ec900b7645638b14e86a1ca3073d3acc   |
| 2 | team        | string    | No       | Full name of the basketball team                        |             | Los Angeles Lakers                 |
| 3 | team_abbr   | string    | No       | Abbreviation of the team name                           |             | LAL                                |
| 4 | arena_sk    | string    | No       | Surrogate key generated using MD5 hash of the arena     | FK          | 8b8c324c412f94b2e08719d9f8db29d0   |
