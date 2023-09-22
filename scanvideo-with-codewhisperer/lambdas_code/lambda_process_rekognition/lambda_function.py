#create a function to get content moderation from jobid from rekognition
import boto3
import json
import os

bucket_name = os.environ.get('BUCKET_NAME')
rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

def get_content_moderation(job_id, rekognition_client):
    response = rekognition_client.get_content_moderation(JobId=job_id)
    return response
#upload response to s3 bucket
def upload_to_s3(bucket, key, response,s3_client):
    s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(response))
    return response
#get jobid from event sns message
def get_jobid(event):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    return message['JobId'] 

#get object name from event sns message
def get_object_name(event):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    return message['Video']['S3ObjectName']

#create a lambda function to get content moderation from rekognition
def lambda_handler(event, context):
    jobid = get_jobid(event)
    object_name = get_object_name(event)
    filename = object_name.split("/")[-1].replace(".mp4", ".json")
    key = "moderation-file/"+filename
    print(jobid)
    response = get_content_moderation(jobid, rekognition_client)
    print(response)
    upload_to_s3(bucket_name, key, response,s3_client)
    return response
