import json
import random
import boto3
from botocore.config import Config

def lambda_handler(event, context):
    client = boto3.client('ssm')

    images_bucket = client.get_parameter(Name='YestImagesS3Bucket')["Parameter"]["Value"]

    s3Client = boto3.client('s3', region_name='us-west-2', config = Config(s3={'addressing_style': 'virtual'}))
    id = random.randrange(10000000)
    filename = str(id) + ".jpg"
    response = s3Client.generate_presigned_post(images_bucket, filename, Fields=None, Conditions=None, ExpiresIn=3600)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE'}
    }
