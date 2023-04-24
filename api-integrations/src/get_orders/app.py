import boto3
import os
import json
from typing import Dict, Any

ddb_client = boto3.client("dynamodb")
TABLE_NAME = os.environ.get("ORDER_TABLE")

def fetch_all_orders(dynamo_client, table_name):
    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = dynamo_client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else:
            response = dynamo_client.scan(TableName=table_name)
            
        last_evaluated_key = response.get('LastEvaluatedKey')

        results.extend(response['Items'])

        if not last_evaluated_key:
            break
    print(f'fetch_all_orders returned {results}')
    return results


def handler(event, context):
    items = fetch_all_orders(ddb_client, TABLE_NAME)
    return {  
        "statusCode": 200,
        "body": json.dumps(items, indent=4)
    }





