from __future__ import print_function
import boto3, botocore, sys
from datetime import datetime
import subprocess

def print_usage():
    print("This is a python script to copy necessary RDS logs to s3\n" + \
                                "example as: python3 abc.py bucketname rdsinstancename region rdsendpoint rdsuser rdspass")

def parse_args(args):
    if len(sys.argv) == 7:
        return True
    else:
        print ("ERROR: Invalid command line arguments")
        print_usage()
        return False

def copy_logs_from_RDS_to_S3():

    S3BucketName = sys.argv[1] 
    RDSInstanceName = sys.argv[2]
    region = sys.argv[3]
    arr = ["error", "slow", "general", "bin"]
   # logNamePrefix = "error"
    
    # initialize
    RDSclient = boto3.client('rds',region_name=region)
    S3client = boto3.client('s3',region_name=region)
    lastWrittenTime = 0
    lastWrittenThisRun = 0
    backupStartTime = datetime.now()
    
    # check if the S3 bucket exists and is accessible
    try:    
        S3response = S3client.head_bucket(Bucket=S3BucketName)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['ResponseMetadata']['HTTPStatusCode'])
        if error_code == 404:
            print ("Error: Bucket name provided not found")
            return
        else:	
            print ("Error: Unable to access bucket name, error: " + e.response['Error']['Message'])
            return
    
    try:
        S3response = S3client.get_object(Bucket=S3BucketName, Key=RDSInstanceName)
        lastWrittenTime = int(S3response['Body'].read(S3response['ContentLength']))
        print("Found marker from last log download, retrieving log files with lastWritten time after %s" % str(lastWrittenTime))
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['ResponseMetadata']['HTTPStatusCode'])
        if error_code == 404:
            print ("It appears this is the first log import, all files will be retrieved from RDS")
        else:
            print ("Error: Unable to access config file, error: " + e.response['Error']['Message'])
            return


    copiedFileCount = 0
    logMarker = ""
    moreLogsRemaining = True
    while moreLogsRemaining:
        for x in arr:
            print(x)
            logNamePrefix = x
            current_date = datetime.today().strftime('%Y-%m-%d')
            dbLogs = RDSclient.describe_db_log_files(DBInstanceIdentifier=RDSInstanceName, FilenameContains=logNamePrefix, FileLastWritten=lastWrittenTime, Marker=logMarker)
            if 'Marker' in dbLogs and dbLogs['Marker'] != "":
                logMarker = dbLogs['Marker']
            else:
                moreLogsRemaining = False

	# copy the logs in this batch
            for dbLog in dbLogs['DescribeDBLogFiles']:
                print ("FileNumber: ", copiedFileCount + 1)
                print("Downloading log file: %s found and with LastWritten value of: %s " % (dbLog['LogFileName'],dbLog['LastWritten']))
                if int(dbLog['LastWritten']) > lastWrittenThisRun:
                    lastWrittenThisRun = int(dbLog['LastWritten'])
                logFileData = ""
                try:
                    logFile = RDSclient.download_db_log_file_portion(DBInstanceIdentifier=RDSInstanceName, LogFileName=dbLog['LogFileName'],Marker='0')
                    logFileData = logFile['LogFileData']
                    while logFile['AdditionalDataPending']:
                        logFile = RDSclient.download_db_log_file_portion(DBInstanceIdentifier=RDSInstanceName, LogFileName=dbLog['LogFileName'],Marker=logFile['Marker'])
                        logFileData += logFile['LogFileData']
                except Exception as e:
                    print ("File download failed: ", e)
                    continue
                logFileDataCleaned = logFileData.encode(errors='ignore')
                logFileAsBytes = str(logFileDataCleaned).encode()

		# upload the log file to S3
                objectName = RDSInstanceName + "/" + current_date + "/" + backupStartTime.isoformat() + "/" + dbLog['LogFileName']
                try:
                    S3response = S3client.put_object(Bucket=S3BucketName, Key=objectName,Body=logFileAsBytes)
                    copiedFileCount += 1
                except botocore.exceptions.ClientError as e:
                    print ("Error writting object to S3 bucket, S3 ClientError: " + e.response['Error']['Message'])
                    return
                print("Uploaded log file %s to S3 bucket %s" % (objectName,S3BucketName))

        print ("Copied ", copiedFileCount, "file(s) to s3")

def copy_binlogs_from_RDS_to_S3():

    S3BucketName = sys.argv[1]
    RDSInstanceName = sys.argv[2]
    RDSEndpoint = sys.argv[4]
    RDSUser = sys.argv[5]
    RDSPass = sys.argv[6]

    
if(parse_args(sys.argv)):
    copy_logs_from_RDS_to_S3()
    copy_binlogs_from_RDS_to_S3()
