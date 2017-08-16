import json
import urllib.parse
import boto3

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
    json_dict = json.loads(body)
        
    return json_dict

def lambda_handler(event, context):
    # prefix用に年月取得
    now = datetime.datetime.now()
    year = str(now.strftime('%Y'))
    month = str(now.strftime('%m'))

    # パラメータが不正な場合のデフォルトを荒川に
    if (set(event) >= {'country', 'prefectures', 'river'}):
        country = event['country'] if len(event['country']) != 0 else 'japan'
        prefectures = event['prefectures'] if len(event['prefectures']) != 0 else 'tokyo'
        river = event['river'] if len(event['river']) != 0 else 'arakawa'
        prefix = target + '/' + country + '/' + prefectures + '/' + river + '/' + year + '/' + month + '/'
    else:
        prefix = 'rainFall/japan/tokyo/arakawa/' + year + '/' + month + '/'
    
    try:
        # 最新のファイル名を取得
        target_key = get_latest_keyname(prefix)
        # ファイル名をkeyとしてS3からデータ取得
        json_dict = get_rainfall(target_key)
        
        return json_dict
    except Exception as e:
        print(e)
        # print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        return 'InternalServerError'
