from datetime import datetime
import boto3
import uuid
import os
import json
import decimal

TABLE_NAME = os.environ.get("ORDER_TABLE")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def update_order(order_id, request_payload):
    now = datetime.now()

    get_item_response = table.get_item(
        Key={
            'id': order_id,
            'user_id': 'demo_user'
        }
    )

    if 'Item' in get_item_response:
        print(f'update_order ddb get_item: {order_id} returned: {get_item_response}')
        response = table.update_item(
            Key={
                'id': order_id,
                'user_id': 'demo_user'
            },
            ExpressionAttributeNames={
                "#nm": "name"
            },
            ExpressionAttributeValues={
                ":n": request_payload["name"],
                ":q": request_payload["quantity"],
                ":r": request_payload["restaurantId"],
                ":u": now.isoformat()
            },
            UpdateExpression="set quantity = :q, #nm = :n, restaurantId = :r, updatedAt = :u",
            ReturnValues="UPDATED_NEW"
        )
        print(f'update_order ddb update_item response {response}') 
        update_order_response = {'message': 'update success', 'id': order_id, 'updated_values': response['Attributes']}
        return update_order_response
    else:
        return {'message': f'order {order_id} not found'}


def handler(event, context):
    order_id = event['pathParameters']['orderId']
    request_payload = json.loads(event["body"])
    response = update_order(order_id, request_payload)
    print(f'update_order_response: {response}')
    return {  
        'statusCode': 200,
        'body': json.dumps(response, indent=4, cls=DecimalEncoder)
    }





