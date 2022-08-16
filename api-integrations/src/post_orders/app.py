from datetime import datetime
import boto3
import uuid
import os
import json
import decimal

#TABLE_NAME = os.environ.get('ORDER_TABLE')
DEFAULT_ORDER_STATUS = "PENDING"
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")
sfn = boto3.client("stepfunctions")
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(TABLE_NAME)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def assemble_order(message_id, order_data):
    now = datetime.now()
    order_data["user_id"] = "demo_user"
    order_data["id"] = message_id
    order_data["orderStatus"] = DEFAULT_ORDER_STATUS
    order_data["createdAt"] = now.isoformat()
    return json.dumps(order_data,cls=DecimalEncoder)

def start_sfn_exec(sfn_input, sfn_exec_id):
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=sfn_exec_id,
        input=json.dumps(sfn_input,cls=DecimalEncoder)
    )
    print(f'post_orders start sfn_exec_id {sfn_exec_id} and input {sfn_input}')
    return response

def handler(event, context):
    new_order_list = []
    for record in event["Records"]:
        message_id = record["messageId"]
        request_body = json.loads(record["body"])
        order_data = request_body["data"]
        print(f'post_orders reqeust_body {order_data} type: {type(order_data)}')
        sfn_input = assemble_order(message_id, order_data)
        response = start_sfn_exec(sfn_input, message_id)
        print(f'start sfn execution: {response}')
        new_order_list.append(response["executionArn"])
    return {  
        "statusCode": 200,
        "body": json.dumps(new_order_list, indent=4)
    }





