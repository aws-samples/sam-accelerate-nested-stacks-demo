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

def update_order(order_status, error_message, event):
    response = table.update_item(
        Key={
            "user_id": event["saveResults"]["user_id"],
            "id": event["saveResults"]["id"]
            },
        UpdateExpression="set orderStatus = :s, errorMessage = :m",
        ExpressionAttributeValues={
            ":s": order_status,
            ":m": error_message
            },
        ReturnValues="UPDATED_NEW"
    )
    
    message = {"order_status": order_status, "order_id": event["saveResults"]["id"], "cancel_reason": error_message}
    send_order_notification(message)
    print(f'Order canceled sent {message}')
    
    return {
        "statusCode": 200,
        "body": "Order canceled and notification sent"
    }

def send_order_notification(message):
    topic_arn = TOPIC_ARN
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        Subject='Orders-App: order notification'
    ) 

def handler(event, context):
    print(f'event: {event}')
    order_status = "FAILED"
    error_message = event["paymentResult"]["error_message"]
    response = update_order(order_status, error_message, event)
    print(f'update_order.response: {response}')
    return response




