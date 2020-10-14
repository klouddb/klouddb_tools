# PostgreSQL backups

Amazon RDS for PostgreSQL generates query and error logs. RDS PostgreSQL writes autovacuum information and rds_admin actions to the error log. PostgreSQL also logs connections, disconnections, and checkpoints to the error log

Inorder to generate query logs you need to enable log_statement and log_min_duration_statement. Log_statement can be set to none/all/mod. None is the default which does not log any queries . All option logs all types of queries and mod only records DML statements. log_min_duration_statement can be used to set the cutoff time for queries . For example : If you are interested in queries taking more than 10 seconds , you can set log_min_duration_statement to 10 seconds


Below is a sample set of files that you can retrieve from RDS PostgreSQL :

```
aws --output text rds describe-db-log-files --db-instance-identifier postgres-1  --region us-east-2
DESCRIBEDBLOGFILES      1600869540000   error/postgres.log      5875
DESCRIBEDBLOGFILES      1600869540000   error/postgresql.log.2020-09-23-13      2174
DESCRIBEDBLOGFILES      1600869900000   error/postgresql.log.2020-09-23-14      654
[root@ip-172-31-35-8 ec2-user]#
```
NOTE:  Binary log code is only applicable to MySQL logs. Unfortunately RDS PostgreSQL does not allow us to download WAL files yet 

## How to execute the code ?

Example :python3 rdspostgreslogs.py bucketname rdsinstancename region rdsendpoint rdsuser rdspass
```
bucketname  =>  s3 bucket where you want to save your backups
rdsinstance =>  Your rds instanceid
region      =>  AWS region e.g : us-east-1
rdsendpoint =>  Your rds instance endpoint
rdsuser     =>  User is required to retrieve binary logs(MySQL)
rdspass     =>  Password for rdsuser
```

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

## How to execute the code ?

Example :python3 rdsmysqllogs.py bucketname rdsinstancename region rdsendpoint rdsuser rdspass

```
bucketname  =>  s3 bucket where you want to save your backups
rdsinstance =>  Your rds instanceid
region      =>  AWS region e.g : us-east-1
rdsendpoint =>  Your rds instance endpoint
rdsuser     =>  User is required to retrieve binary logs(MySQL)
rdspass     =>  Password for rdsuser
```
