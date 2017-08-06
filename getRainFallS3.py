import json
import urllib.parse
import boto3

client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = 'test-uodu-s3'
    prefix = 'sample_json/'

    try:
        # 一覧を取得
        list = client.list_objects(
            Bucket='test-uodu-s3',
            Prefix='sample_json/kanazawa'
        )
        if 'Contents' in list:
            keys = {}
            for content in list['Contents']:
                keys[content['Key']] = content['LastModified']
    
        # 最も新しいファイルを取得
        target_key = max(keys, key=(lambda x: keys[x]))
        
        response = client.get_object(Bucket=bucket, Key=target_key)

        body = response['Body'].read().decode('utf-8')
        result = json.loads(body)
        return result
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

