# Db utility to create pagila , postgres_air , dvdrental and pgbench sample dbs



## Usage

* create the `.env` file from `env.example` and change the required password and username etc. 
* Run `python execute.py` as the script

## Functionality

* It works for 4 databases: 
  * [pagila](https://github.com/devrimgunduz/pagila) with [ER Diagram](https://github.com/klouddb/testshivam/blob/main/erdiagrams/pagilaERdiagram.png)
  * pgbench with [ER Diagram](https://github.com/klouddb/testshivam/blob/main/erdiagrams/pgbench_sampledb_ERdiagram.png)
  * [dvdrental](https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/) with [ER Diagram](https://github.com/klouddb/testshivam/blob/main/erdiagrams/dvdrentalschema.png)
  * [postgres_air](https://github.com/hettie-d/postgres_air) with [ER Diagram](https://github.com/klouddb/testshivam/blob/main/erdiagrams/postgres_air_er_diagram.png). pls read the [these](https://github.com/klouddb/testshivam/blob/main/postgres_air/README.md) steps before running the script for postgres_air database.
* Script will ask for the database name for which user wants to perform the action, valid options are: `[pagila, sampledb, dvdrental, postgres_air]`. If you wan to use `pgbench` then enter `sampledb`
* If the database already exists then script will ask to drop the database, if type `True` then script will drop the database and exit
* If Any invalid option given then script will exit

