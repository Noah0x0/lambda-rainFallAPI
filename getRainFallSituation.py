import json
import urllib.parse
import boto3

client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = 'test-uodu-s3'
    key = 'rain_fall_situation.json'

    try:
        response = client.get_object(Bucket=bucket, Key=key)

        body = response['Body'].read().decode('utf-8')
        result = json.loads(body)
        return result
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
