# dbutil.py
# Purpose : Simple DB Utility to get data from Postgresql and Compare the Settings

import sys, psycopg2
import os
import json
from datetime import datetime

conn=None
cur=None

def load_env(env_file):
  with open(env_file) as f:
      for line in f:
          if line.startswith('#') or not line.strip():
              continue
          key, value = line.strip().split('=', 1)
          os.environ[key]=value
        
def close_db_conn(conn):
  if conn is not None:
    conn.close()
  
def get_config(config_index):
  db_config={}
  db_config["host"]=os.environ[f"DB{config_index}_HOSTNAME"]
  db_config["dbname"]=os.environ[f"DB{config_index}_NAME"]
  db_config["user"]=os.environ[f"DB{config_index}_USERNAME"]
  db_config["password"]=os.environ[f"DB{config_index}_PASSWORD"]
  db_config["port"]=os.environ[f"DB{config_index}_PORT"]  
  print(db_config)
  return db_config
   

def get_db_conn(db_config_index):
  global conn
  config_params=get_config(db_config_index)
  conn = psycopg2.connect(**config_params)  
  cur = conn.cursor()
  return cur


def get_settings_data(host_index):
  try:
    cur=get_db_conn(host_index)
    cur.execute('''select * from pg_settings;''')
    results=cur.fetchall()
    setting_values={}
    for item in results:
      setting_values[item[0]]=item[1]

    cur.close()
    return setting_values
  except (Exception, psycopg2.DatabaseError) as error:
      print(error)
  finally:
      close_db_conn(conn)

def compare_values(settings1_dict,settings2_dict):
  diffkeys = [k for k in settings1_dict if settings1_dict[k] != settings2_dict[k]]
  return diffkeys


def format_json(diffkeys, host1_setting, host2_setting, iso_date_time):
    summary = {"total_difference": len(diffkeys), "timestamp": iso_date_time}
    results = {}
    for key in diffkeys:
        results[key] = {"host_1": host1_setting[key],
                        "host_2": host2_setting[key]}
    summary["diffs"] = results
    return summary


if __name__ == '__main__':
    load_env(".env")
    host1_setting = get_settings_data(1)
    host2_setting = get_settings_data(2)
    diffkeys=compare_values(host1_setting,host2_setting)
    # Print in Plain text
    for k in diffkeys:
      print(k, ':', host1_setting[k], '->', host2_setting[k])

    # Print in JSON
    diffkeys = compare_values(host1_setting, host2_setting)
    iso_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    iso_time=datetime.now().strftime('%H%M%S%f%z')
    iso_date = datetime.now().strftime('%Y-%m-%d')
    formatted = format_json(diffkeys, host1_setting,host2_setting, iso_date_time)  
    print(json.dumps(formatted))


