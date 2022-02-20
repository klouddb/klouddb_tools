#!/bin/bash
RDSUser=$1
RDSEndpoint=$2
RDSPass=$3
RDSName=$5
current_date=`date +"%F"`
current_time_iso=`date -Iseconds`
s3bucket=$4
mysql_binlog_filename=$(mysql -u $RDSUser -h $RDSEndpoint -p$RDSPass -e "show master logs"|grep "mysql-bin"|awk '{print $1}')

mkdir -p $current_date/$current_time_iso/binary
for file in $mysql_binlog_filename
do
        mysqlbinlog -u $RDSUser -h $RDSEndpoint -p$RDSPass --read-from-remote-server $file --result-file=$current_date/$current_time_iso/binary/$file
done

aws s3 sync ./$current_date s3://$s3bucket/$RDSName/$current_date
