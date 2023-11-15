#!/bin/python3

import boto3
import json
import urllib.parse

region = "us-east-2"
s3 = boto3.client('s3', region_name=region)

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        print(f'[+] Retrieving Object {key} from {bucket}')
        response = s3.get_object(Bucket=bucket, Key=key)
        print(f'[+] Object {key} Retrieved from {bucket}')
        return {
            'statusCode': 200,
            'body': json.dumps({'Object Response': response})
        }
    except Exception as e:
        print(f'[-] Error Retreiving Object {key} from {bucket}')
        print(e)
        raise e