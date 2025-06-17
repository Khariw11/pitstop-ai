import boto3 #AWS SDK to access CLoodWatch logs 
import json #to save logs as JSON
import os #to create directories 


#1. Create Client for CLoudwatch logs 
logs_client = boto3.client('logs')

#2. Define main log fetching function
def fetch_logs(log_group, limit=1000):
    #3. get latest log stream
    response = logs_client.describe_log_streams(
        logGroupName=log_group,
        orderBy='LastEventTime',
        descending=True,
        limit=1
    )
# Pull most recent stream name 
    log_stream_name = response ['logStreams'][0]['logStreamName']

#4. Get log events from stream
    log_events = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream_name,
        limit=limit,
        startFromHead=True
    )

#5. Extract only the message field from each event.
    logs = [event['message'] for event in log_events['events']]

#6. save logs locally 
    
    os.makedirs('data/raw_logs', exist_ok=True)
    with open('data/raw_logs/sample_logs.json', 'w') as f:
        json.dump(logs, f)

    print(f"[√] {len(logs)} logs saved to data/raw_logs/sample_logs.json")
    return logs 

#For Testing

if __name__ == '__main__':
    #Plug-in your log group name here
    fetch_logs(log_group='YOUR_LOG_GROUP_NAME_HERE')
    