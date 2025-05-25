## Data Dictionary: `dim_arena` table.

| # | column_name | data_type | nullable | description                                              | constraints | example                          |
|---|-------------|-----------|----------|----------------------------------------------------------|-------------|----------------------------------|
| 1 | arena_sk    | string    | No       | Surrogate key generated using MD5 hash of the arena name | PK          | 6153edbe6543c382a4fd9752e70d102f |
| 2 | arena       | string    | No       | Name of the team's arena                                 |             | Milwaukee Arena                  |
