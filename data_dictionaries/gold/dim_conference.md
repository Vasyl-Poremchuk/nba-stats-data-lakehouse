## Data Dictionary: `dim_conference` table.

| # | column_name   | data_type | nullable | description                                                                     | constraints | example                          |
|---|---------------|-----------|----------|---------------------------------------------------------------------------------|-------------|----------------------------------|
| 1 | conference_sk | string    | No       | Surrogate key generated using MD5 hash of the conference name (e.g., `Eastern`) | PK          | 988c64336b8b535611fc1f617eca2cef |
| 2 | conference    | string    | No       | Name of the conference                                                          |             | Western                          |
| 3 | division_sk   | string    | No       | Surrogate key generate using MD5 hash of the division name within a conference  | FK          | f17af17f6b59b4e7f1d4a6e99fbf7675 |
