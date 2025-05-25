## Data Dictionary: `dim_season` table.

| # | column_name   | data_type | nullable | description                                                                | constraints | example                           |
|---|---------------|-----------|----------|----------------------------------------------------------------------------|-------------|-----------------------------------|
| 1 | season_sk     | string    | No       | Surrogate key generated using MD5 hash of the season                       | PK          | 0a19f101b49d5e2816d7568fc29280e9  |
| 2 | season        | string    | No       | Season identifier                                                          |             | 2017-18                           |
| 3 | league        | string    | No       | Name of the basketball league                                              |             | NBA                               |
| 4 | year          | bigint    | No       | End year of the season                                                     |             | 2018                              |
| 5 | conference_sk | string    | No       | Surrogate key generated using MD5 hash of the conference (e.g., `Eastern`) | FK          | 988c64336b8b535611fc1f617eca2cef  |
