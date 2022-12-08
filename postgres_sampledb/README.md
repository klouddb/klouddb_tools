# Db utility to create pagila , postgres_air , dvdrental and pgbench sample dbs



## Usage

* create the `.env` file from `env.example` and change the required password and username etc. 
* Run `python execute.py` as the script

Please check our blog https://klouddb.io/db-utility-to-deploy-4-postgres-sample-dbs-pagilapostgres_airdvdrentalpgbench/ for detailed walkthrough
## Functionality

* It works for 4 databases: 
  * [pagila](https://github.com/devrimgunduz/pagila) with [ER Diagram](https://github.com/klouddb/klouddb_tools/blob/main/postgres_sampledb/erdiagrams/pagilaERdiagram.png)
  * pgbench with [ER Diagram](https://github.com/klouddb/klouddb_tools/blob/main/postgres_sampledb/erdiagrams/pgbench_sampledb_ERdiagram.png)
  * [dvdrental](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) with [ER Diagram](https://github.com/klouddb/klouddb_tools/blob/main/postgres_sampledb/erdiagrams/dvdrentalschema.png)
  * [postgres_air](https://github.com/hettie-d/postgres_air) with [ER Diagram](https://github.com/klouddb/klouddb_tools/blob/main/postgres_sampledb/erdiagrams/postgres_air_er_diagram.png). 
* Script will ask for database name : `[pagila, sampledb, dvdrental, postgres_air]`. If you want to use `pgbench` then enter `sampledb`


