#!/usr/bin/python
import os, psycopg2, sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def load_env(env_file):
  with open(env_file) as f:
      for line in f:
          if line.startswith('#') or not line.strip():
              continue
          key, value = line.strip().split('=', 1)
          os.environ[key]=value


def get_config():
  db_config={}
  db_config["host"]=os.environ["db_hostname"]
  db_config["dbname"]=os.environ["db_name"]
  db_config["user"]=os.environ["db_username"]
  db_config["password"]=os.environ["db_password"]
  db_config["port"]=os.environ["db_port"]
  return db_config

def get_db_conn(database_name):
  global conn
  config_params=get_config()
  dbname = database_name
  conn = psycopg2.connect(**config_params)  
  cur = conn.cursor()
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  return cur

def connect():
    name = input("Please enter the database name you want to create, options are pagila, sampledb, dvdrental, postgres_air:")
    conn = None
    try:
        cur=get_db_conn("postgres")
        if name.lower() in ['pagila', 'sampledb', 'dvdrental', 'postgres_air']:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{0}'".format(name))
            exists = cur.fetchone()
            if not exists:
                print('creating the Database', name)
                cur.execute('CREATE DATABASE {0}'.format(name))
                if name.lower() == 'pagila':
                    os.chdir('./pagila')
                    os.environ['PGPASSWORD'] = os.environ['db_password']
                    os.environ['PGUSER'] = os.environ['db_username']
                    os.environ['PGHOST'] = os.environ['db_hostname']
                    os.environ['PGPORT'] = os.environ['db_port']
                    print('INSERT pagila-schema.sql NOW')
                    os.system('psql -d pagila -f pagila-schema.sql')
                    print('INSERT pagila-insert-data.sql NOW')
                    os.system('psql -d pagila -f pagila-insert-data.sql')
                    cur.close()
                elif name.lower() == 'sampledb':
                    os.environ['PGPASSWORD'] = os.environ['db_password']
                    os.environ['PGUSER'] = os.environ['db_username']
                    os.environ['PGHOST'] = os.environ['db_hostname']
                    os.environ['PGPORT'] = os.environ['db_port']
                    expected_size = int(input("enter the size of the database you want in GBs Example 5:"))
                    scaling_factor = int(round(expected_size / 0.015625))
                    print("scaling factor will be {0} for the choose db size".format(scaling_factor))
                    os.system('pgbench -i -s {0} -d sampledb'.format(scaling_factor))
                elif name.lower() == 'dvdrental':
                    os.chdir('./dvdrental')
                    os.environ['PGPASSWORD'] = os.environ['db_password']
                    os.environ['PGUSER'] = os.environ['db_username']
                    os.environ['PGHOST'] = os.environ['db_hostname']
                    os.environ['PGPORT'] = os.environ['db_port']
                    print('INSERT data NOW')
                    os.system('pg_restore -d dvdrental dvdrental.tar')
                    cur.close()
                elif name.lower() == 'postgres_air':
                    os.chdir('./postgres_air')
                    print('unzipping the postgres air file. pls wait it will take 5-10 mins')
                    os.system('unzip postgres_air.zip')
                    os.environ['PGPASSWORD'] = os.environ['db_password']
                    os.environ['PGUSER'] = os.environ['db_username']
                    os.environ['PGHOST'] = os.environ['db_hostname']
                    os.environ['PGPORT'] = os.environ['db_port']
                    print('INSERT data NOW')
                    os.system('psql -d postgres_air -f postgres_air.sql')
                    cur.close()
            else:
                print("'{0}' is already exists".format(name))
                action = input("Do you want to delete the database ? True or False?")
                if action == 'True':
                    print('Deleting database {0}. now the existing database is deleted . Please validate and try this operation again'.format(name))
                    cur.execute('DROP DATABASE {0}'.format(name))
                    if name.lower() == 'pagila':
                        cur2 = get_db_conn("pagila")
                        print("delete the schema now")
                        cur2.execute('DROP SCHEMA IF EXISTS pagilaschema CASCADE;')
                elif action == 'False':
                    print('No Action taken')
        else:
            print('database name should be in pagila, sampledb, dvdrental, postgres_air')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    load_env(".env")
    connect()


