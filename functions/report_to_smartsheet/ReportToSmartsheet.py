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
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print(f'[-] Error: Invalid Status Code Retrieving Object {key} from {bucket}')
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'error': 'Invalid Status Code Retrieving Object' + key + ' from '+ bucket
            }
        
    except Exception as e:
        print(f'[-] Error Retreiving Object {key} from {bucket}')
        print(e)
        raise e

    data = response['Body'].read().decode('utf-8')
    
    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
        'body': data
    }