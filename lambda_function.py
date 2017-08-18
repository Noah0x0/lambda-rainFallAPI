import json
import urllib.parse
import boto3
import datetime

bucket = 'test-uodu-s3'
target = 'rainFall'

client = boto3.client('s3')

def get_latest_keyname(prefix):
    # 国・都道府県・川名別の一覧を取得
    list = client.list_objects(
        Bucket=bucket,
        Prefix=prefix
    )
    
    # 最も更新日が新しいものを取得
    if 'Contents' in list:
        keys = {}
        for content in list['Contents']:
            keys[content['Key']] = content['LastModified']
    target_key = max(keys, key=(lambda x: keys[x]))
    
    return target_key

def get_rainfall(target_key):
    response = client.get_object(Bucket=bucket, Key=target_key)
    body = response['Body'].read().decode('utf-8')
    return body

def set_response_body(status_code, body):
    headers = {}
    headers['Content-Type'] = 'application/json'

    res_body = {}
    res_body['statusCode'] = status_code
    res_body['headers'] = headers
    res_body['body'] = body
    
    return res_body

def lambda_handler(event, context):
    # prefix用に年月取得
    now = datetime.datetime.now()
    year = str(now.strftime('%Y'))
    month = str(now.strftime('%m'))

    # クエリが渡されてない場合
    if (event['queryStringParameters'] is None):
        return set_response_body(400, 'Bad Request')
    else:
        params = event['queryStringParameters']
        
    # クエリパラメータが不正な場合のデフォルトを荒川に
    if (set(params) >= {'country', 'prefectures', 'river'}):
        country = params['country']
        prefectures = params['prefectures']
        river = params['river']
        prefix = target + '/' + country + '/' + prefectures + '/' + river + '/' + year + '/' + month + '/'
    else:
        return set_response_body(400, 'Bad Request')
    
    try:
        # 最新のファイル名を取得
        target_key = get_latest_keyname(prefix)
        # ファイル名をkeyとしてS3からデータ取得
        json_str = get_rainfall(target_key)
        
        return set_response_body(200, json_str)
    except Exception as e:
        print(e)
        return set_response_body(400, 'Bad Request')
