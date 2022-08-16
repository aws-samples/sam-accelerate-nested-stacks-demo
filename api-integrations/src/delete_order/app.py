import boto3
import os
import json
import decimal
from typing import Dict, Any

TABLE_NAME = os.environ.get("ORDER_TABLE")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def delete_order(event):
    order_id = event['pathParameters']['orderId']
    response = table.delete_item(
        Key={
            'id': order_id,
            'user_id': 'demo_user'
        }
    )
    print(f'delete_order {order_id} response: {response}')
    return response

def handler(event, context):
    """Handler function integrated with 
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    response = delete_order(event)   
    return {  
        "statusCode": 204,
        "body": json.dumps(response, indent=4, cls=DecimalEncoder)
    }
    





