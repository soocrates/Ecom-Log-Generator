import json
import boto3
import uuid
from main import generate_logs

STREAM_NAME = ""

def get_data(per_second, duration):
    return generate_logs(per_second, duration)
  
def generate(stream_name, kinesis_client, per_second, duration):
    log_generator = get_data(per_second, duration)
    count = 0  # Initialize counter
    for data in log_generator:
        try:
            response = kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(data),
                PartitionKey=str(uuid.uuid4())
            )
            count += 1  # Increment counter after successful send
            print(f"Record {count}: Data sent to Kinesis = {data}")  # Print the counter
        except Exception as e:
            print(f"Error sending record: {e}")
        

if __name__ == '__main__':
    logs_per_second = int(input("Enter the number of logs per second: "))
    duration_seconds = int(input("Enter the duration in seconds: "))
    generate(STREAM_NAME, boto3.client('kinesis', region_name='us-east-1'), logs_per_second, duration_seconds)