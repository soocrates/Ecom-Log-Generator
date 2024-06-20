import json
import boto3
import uuid
from main import generate_logs
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
STREAM_NAME = os.getenv('STREAM_NAME')
LOGS_PER_SECOND = int(os.getenv('LOGS_PER_SECOND', 20))  # Default to 20 if not set
LOGS_DURATION = int(os.getenv('LOGS_DURATION', 60))  # Default to 60 seconds if not set

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
    generate(STREAM_NAME, boto3.client('kinesis', region_name=AWS_REGION), LOGS_PER_SECOND, LOGS_DURATION)