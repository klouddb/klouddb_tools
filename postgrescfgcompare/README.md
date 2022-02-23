
# Populate config file before comparing 

You need to populate below environment variables . You can put all of below variables in a hidden file called .env and source it . You can issue a command like ‘echo $DB1_HOSTNAME’ to see if the variables are properly initialized

DB1_HOSTNAME=Hostname/ip of first hostname

DB1_USERNAME= username of first hostname

DB1_PASSWORD= password of first hostname

DB1_NAME=postgres

DB1_PORT=5432 (change port depending on your config)

DB2_HOSTNAME=Hostname/ip of second hostname

DB2_USERNAME=username of first hostname

DB2_PASSWORD= password of second hostname

DB2_PORT=5432(change port depending on your config)

DB2_NAME=postgres

# Execute script 

Once above environment variables are loaded please execute the script ‘python3 pgcfgcompare.py’


Sample output :

Below is a sample output  . Differences between below two hosts are displayed . Some differences like transaction_read_only and primary_conninfo can be ignored as one of them is replica . Replicas have read_only enabled and primary_conninfo values which is totally fine . But the other differences needs to be addressed


{'host': '18.xxx.xx.xxx', 'dbname': 'postgres', 'user': 'repusrr', 'password': 'xxx', 'port': '5432'}
{'host': '3.xxx.xx.xxx', 'dbname': 'postgres', 'user': 'repusrr', 'password': 'xxx', 'port': '5432'}
data_directory_mode : 0750 -> 0700
primary_conninfo : user=replicator password=replicator host=3.22.209.122 port=5432 
server_version : 12.4 -> 12.7
transaction_read_only : on -> off
