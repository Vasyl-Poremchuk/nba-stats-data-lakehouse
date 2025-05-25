## Data Dictionary: `dim_division` table

| # | column_name | data_type | nullable | description                                                                     | constraints | example                           |
|---|-------------|-----------|----------|---------------------------------------------------------------------------------|-------------|-----------------------------------|
| 1 | division_sk | string    | No       | Surrogate key generated using MD5 hash of the division name                     | PK          | f17af17f6b59b4e7f1d4a6e99fbf7675  |
| 2 | division    | string    | No       | Name of the division withing a conference                                       |             | Atlantic                          |
| 3 | team_sk     | string    | No       | Surrogate key generated using MD5 hash of the team name (e.g., `Chicago Bulls`) | FK          | e938c5bbd29de26c3a600a0330465f8b  |
