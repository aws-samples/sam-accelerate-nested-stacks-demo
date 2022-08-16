import boto3
import os
import decimal
import json

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

def update_order(order_status, event):

    response = table.update_item(
        Key={
            "user_id": event["saveResults"]["user_id"],
            "id": event["saveResults"]["id"]
            },
        UpdateExpression="set orderStatus = :s",
        ExpressionAttributeValues={
            ":s": order_status
            },
        ReturnValues="UPDATED_NEW"
    )
    message = {"order_status": order_status, "order_id": event["saveResults"]["id"]}
    send_order_notification(message)
    print(f'Order success sent {message}')
    return {
        "statusCode": 200,
        "body": "Order created and notification sent"
    }

def send_order_notification(message):
    '''
    Expects message (type dict) with order_status and order_id values from
    the invoking event.

    {"order_status": SUCCESS, "order_id": b4d27a00-1a73-4089-94f8-87e273b57067}

    Make sns.publish() call using the 'sns' client defined globally.  SNS Topic
    retrieved from Lambda Environment Variable TOPIC_ARN
    '''
    topic_arn = TOPIC_ARN
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        Subject=f'Orders-App: Update for order {message["order_id"]}'
        # Subject='Orders-App: SAM Accelerate for the win!'
    )

def handler(event, context):
    print(f'event: {event}')
    order_status = "SUCCESS"
    response = update_order(order_status, event)
    print(f'update_order response: {response}')
    return response
