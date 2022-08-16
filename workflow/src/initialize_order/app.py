from datetime import datetime
import boto3
import uuid
import os
import json
import decimal

TABLE_NAME = os.environ.get("ORDER_TABLE")
TOPIC_ARN = os.environ.get("TOPIC_ARN")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)
sns = boto3.client("sns")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def persist_order(order_item):
    print(f'persist_order item {order_item} to table {TABLE_NAME}')
    response = table.put_item(Item=order_item)
    message = {"order_status": order_item["orderStatus"], "order_id": order_item["id"]}
    print(f'new order pending payment {message}')
    return {
        "statusCode": 200,
        "body": json.dumps(order_item, indent=4, cls=DecimalEncoder)
    }

def handler(event, context):
    print(f'event contents: {event}')
    create_order_response = persist_order(event)
    print(f'persist_order response: {create_order_response}')
    return create_order_response
