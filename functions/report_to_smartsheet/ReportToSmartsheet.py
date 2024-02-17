#!/bin/python3

import boto3
import urllib.parse
import logging
import smartsheet
import os

FOLDER_ID = "678637063169924"
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

    # with open('/tmp/data.csv', 'w') as file:
    #     file.write(data)

    return data, key.split(".")[0]

# def upload_to_smartsheet(temp_file, sheet_name):
#     try:
#         smart = smartsheet.Smartsheet()
#         smart.errors_as_exceptions(True)
#     except ValueError as e:
#         logger.error(f'[-] Error: SMARTSHEET_ACCESS_TOKEN must be set')
#         raise e
    
#     sheet = smart.Sheets.get_sheet_by_name(sheet_name)
#     if not sheet:
#         logger.info(f'[+] Creating Sheet: {sheet_name}')
#         sheet = smart.Folders.import_csv_sheet(
#             FOLDER_ID, # folder ID
#             temp_file,
#             sheet_name,
#             header_row_index=0,
#             primary_column_index=0,
#         )
#         sheet = smart.Sheets.get_sheet(sheet.data.id)
#         logger.info(f'[+] Sheet {sheet_name} Created')
#         return

#     else:
#         logger.info(f'[+] Attaching New Data to {sheet_name}')

#     os.remove('/tmp/data.csv')

def upload_sheet(sheet):
    try:
        smart = smartsheet.Smartsheet()
        smart.errors_as_exceptions(True)
    except ValueError as e:
        logger.error(f'[-] Error: SMARTSHEET_ACCESS_TOKEN must be set')
        raise e
    logger.info(f'[+] Uploading Sheet: {sheet.name}')
    sheet = smart.Folders.create_sheet_in_folder(
        FOLDER_ID,
        sheet
    )

def create_sheet(sheet_name, data):
    sheet = smartsheet.models.sheet.Sheet()
    sheet.name = sheet_name

    column_headers = data[0]
    logger.info(f'{data[0]}')
    logger.info(f'{sheet}')
    count = 0
    for column_name in column_headers:
        col = smartsheet.models.column.Column()
        if count == 0:
            col.primary = True
        else:
            col.primary = False
        col.title = column_name
        sheet.columns.append(col)
        count += 1
    logger.info(f'{sheet}')
    return sheet



def lambda_handler(event, context):
    logger.info(f'[+] Lambda Invocation Starting')
    data, sheet_name = get_file_from_s3(event)
    sheet = create_sheet(data, sheet_name)
    upload_sheet(sheet)

    return {
        'statusCode': 200,
        'body': '[+] Lambda Invocation Complete'
    }