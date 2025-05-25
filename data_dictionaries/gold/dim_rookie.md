## Data Dictionary: `dim_rookie` table.

| # | column_name           | data_type | nullable | description                                                             | constraints                  | example                          |
|---|-----------------------|-----------|----------|-------------------------------------------------------------------------|------------------------------|----------------------------------|
| 1 | season_sk             | string    | No       | Surrogate key generated using MD5 hash of the season (e.g., `2023-24`)  | PK (part of a composite key) | 2bf5d24e549bc737f012244822cad60f |
| 2 | rookie_of_the_year_sk | string    | No       | Surrogate key generated using MD5 hash of the rookie player's name      | PK (part of a composite key) | 95dc31a50e15183b6bf6c7e3ab90d7c4 |
| 3 | rookie_of_the_year    | string    | No       | Full name of the player awarded rookie of the year for the given season |                              | J. Wilkes                        |
