# RDS MySQL logs

You can fetch error log , slow log , general log via RDS CLI . But inorder to fetch binary logs you need to use something like below. Our script fetches error log, general log , slow log and binary logs and sorts them by timestamp and RDS instance . Script can be further modified to suit your requirements

Below is a sample set of files that you can retrieve from RDS MySQL . NOTE : You do not see binary logs here . Also slow query and general log are only available once you enable them

```
aws --output text rds describe-db-log-files --db-instance-identifier database-1  --region us-east-2
DESCRIBEDBLOGFILES      1600823400000   error/mysql-error-running.log   136
DESCRIBEDBLOGFILES      1600821900000   error/mysql-error-running.log.1 3689
DESCRIBEDBLOGFILES      1600739100000   error/mysql-error-running.log.2 4092
DESCRIBEDBLOGFILES      1600744800000   error/mysql-error-running.log.4 136
DESCRIBEDBLOGFILES      1600823700000   error/mysql-error.log   0
DESCRIBEDBLOGFILES      1599843227000   mysqlUpgrade    1013
DESCRIBEDBLOGFILES      1600822800000   slowquery/mysql-slowquery.log   0
DESCRIBEDBLOGFILES      1600821683000   slowquery/mysql-slowquery.log.1 1561
DESCRIBEDBLOGFILES      1600748310000   slowquery/mysql-slowquery.log.2 2006
```
