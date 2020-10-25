import json
import random
import boto3
from botocore.config import Config

def lambda_handler(event, context):
    client = boto3.client('ssm')

    images_bucket = client.get_parameter(Name='YestImagesS3Bucket')["Parameter"]["Value"]

    s3Client = boto3.client('s3', region_name='us-west-2', config = Config(s3={'addressing_style': 'virtual'}))
    response = s3Client.list_objects_v2(Bucket=images_bucket)
    print(response)
    all = response['Contents']
    
    l = ["http://" + images_bucket + ".s3-us-west-2.amazonaws.com/" + x["Key"] for x in sorted(all, key=lambda a: a["LastModified"], reverse=True)[0:10]]
    print(l)
    
    return {
        'statusCode': 200,
        'body': json.dumps(l),
        'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE'}
    }
