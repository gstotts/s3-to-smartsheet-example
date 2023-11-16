#!/bin/python3

import boto3
import urllib.parse
import logging
import smartsheet

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

    with open('/tmp/data.csv', 'rb') as file:
        file.write(data)

    return '/tmp/data.csv', key.split(".")[0]

def upload_to_smartsheet(temp_file, sheet_name):
    try:
        smart = smartsheet.Smartsheet()
        smart.errors_as_exceptions(True)
    except ValueError as e:
        logger.error(f'[-] Error: SMARTSHEET_ACCESS_TOKEN must be set')
        raise e
    
    sheet = smart.Sheets.get_sheet_by_name(sheet_name)
    if not sheet:
        logger.info(f'[+] Creating Sheet: {sheet_name}')
        sheet = smart.Folders.import_csv_sheet(
            678637063169924, # folder ID
            temp_file,
            sheet_name,
            header_row_index=0,
            primary_column_index=0,
        )
        sheet = smart.Sheets.get_sheet(sheet.data.id)
        logger.info(f'[+] Sheet {sheet_name} Created')
        return

    else:
        logger.info(f'[+] Attaching New Data to {sheet_name}')
        




def lambda_handler(event, context):
    logger.info(f'[+] Lambda Invocation Starting')
    data, sheet_name = get_file_from_s3(event)
    upload_to_smartsheet(data, sheet_name)

    return {
        'statusCode': 200,
        'body': '[+] Lambda Invocation Complete'
    }