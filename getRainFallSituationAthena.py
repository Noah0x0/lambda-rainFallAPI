import boto3
import time
import json

bucket = 'test-uodu-s3'
key = 'rain_fall_situation.json'

def lambda_handler(event, context):
    
    s3_client = boto3.client('s3')
    athena_client = boto3.client('athena', region_name='ap-northeast-1')
    
    response = athena_client.start_query_execution(
        QueryString='SELECT  "現在時刻(分)", "現在値(mm)" FROM rain_fall ORDER BY "現在時刻(月)" DESC, "現在時刻(日)" DESC, "現在時刻(時)" DESC, "現在時刻(分)" DESC LIMIT 10;',
        QueryExecutionContext={'Database': 'kisyou'},
        ResultConfiguration={
            'OutputLocation': "s3://test-uodu-s3/test_athena/athena_results/",
            'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
            }
        })

    time.sleep(50)
    
    result = athena_client.get_query_results(
        QueryExecutionId=response['QueryExecutionId']
    )
    
    rain_fall_situation = []
    tmp_dict = result['ResultSet']['Rows']
    for row in tmp_dict:
        rain_fall_situation.append(row['Data'][1]['VarCharValue'])
    
    # 増加量を判定
    print(rain_fall_situation)
    
    # S3へ
    response = s3_client.put_object(
        ACL='public-read',
        Body=b'{"situation":"up","level":0}',
        #Body=json.dumps(result['ResultSet']['Rows']),
        Bucket=bucket,
        Key=key)
    
    print(result['ResultSet']['Rows'])
    return response


