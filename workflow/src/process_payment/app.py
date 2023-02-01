import boto3
import math
import random

def handler(event, context):
    payment_result = {}
    payment_state = ['ok', 'error']
    error_messages = ['could not reach payment processor', 'payment method declined', 'uknown error']
    payment_random = math.floor(random.random() * len(payment_state))

    if payment_state[payment_random] == "error":
        error_random = math.floor(random.random() * len(error_messages))
        payment_result['error_message'] = error_messages[error_random]

    payment_result['status'] = payment_state[payment_random]

    print(f'payment_result: {payment_result}')
    return payment_result
