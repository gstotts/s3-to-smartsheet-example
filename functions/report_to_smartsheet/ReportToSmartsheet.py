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

    with open('/tmp/data.csv', 'w') as file:
        file.write(data)

    return data, key.split('.')[0]

def create_sheet(data, sheet_name):
    sheet = smartsheet.models.sheet.Sheet()
    sheet.name = sheet_name

    count = 0
    for column_name in (data.splitlines()[0]).split(','):
        col = smartsheet.models.column.Column()
        if count == 0:
            col.primary = True
        else:
            col.primary = False
        col.title = column_name
        col.type = smartsheet.models.enums.column_type.ColumnType.TEXT_NUMBER
        sheet.columns.append(col)
        count += 1

    try:
        smart = smartsheet.Smartsheet()
        smart.errors_as_exceptions(True)
    except ValueError as e:
        logger.error(f'[-] Error: SMARTSHEET_ACCESS_TOKEN must be set')
        raise e
    logger.info(f'[+] Creating Sheet: {sheet.name}')
    result = smart.Folders.create_sheet_in_folder(
        FOLDER_ID,
        sheet
    )

    rows = []
    for row in data.splitlines()[1:]:
        new_row = smartsheet.models.row.Row()
        
        column = 0
        for data in row.split(','):
            cell = smartsheet.models.cell.Cell()
            cell.column_id = result.data.columns[column].id
            cell.value = data
            new_row.cells.append(cell)
            column += 1
        
        rows.append(row)

    sheet = smartsheet.Sheets.get_sheet(result.data.id)
    sheet.add_rows(rows)
            
    return sheet



def lambda_handler(event, context):
    logger.info(f'[+] Lambda Invocation Starting')
    data, sheet_name = get_file_from_s3(event)
    sheet = create_sheet(data, sheet_name)

    return {
        'statusCode': 200,
        'body': '[+] Lambda Invocation Complete'
    }