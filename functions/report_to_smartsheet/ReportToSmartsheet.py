#!/bin/python3

import boto3
import urllib.parse
import logging

region = "us-east-2"
s3 = boto3.client('s3', region_name=region)
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

def get_file_from_s3(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        logger.info(f'[+] Retrieving Object {key} from {bucket}')
        response = s3.get_object(Bucket=bucket, Key=key)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.error(f'[-] Error: Invalid Status Code Retrieving Object {key} from {bucket}')
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'error': 'Invalid Status Code Retrieving Object' + key + ' from '+ bucket
            }
        
    except Exception as e:
        logger.error(f'[-] Error Retreiving Object {key} from {bucket}')
        logger.error(e)
        raise e
    logger.info(f'[+] Successfully Retrieved {key} from {bucket}')

    try:
        data = response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f'[-] Error Reading and Decoding File {key}')
        logger.error(e)
        raise e
    logger.info(f'[+] Successfully read data from {key}')
    return data

def upload_to_smartsheet(data):
    pass

def lambda_handler(event, context):
    logger.info(f'[+] Lambda Invocation Starting')
    data = get_file_from_s3(event)
    upload_to_smartsheet(data)

    return {
        'statusCode': 200,
        'body': '[+] Lambda Invocation Complete'
    }