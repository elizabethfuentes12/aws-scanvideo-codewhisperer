#python code a lambda function to start rekognition video content moderation
import boto3
import json
import os

def lambda_handler(event, context):
    print(event)
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(bucket)
    print(key)
    client = boto3.client('rekognition')
    response = client.start_content_moderation(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        },
        JobTag='rekognition-video-content-moderation'
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    