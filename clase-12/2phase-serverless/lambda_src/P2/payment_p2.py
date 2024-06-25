import json
import random
import utils

service = 'payment'
error_rate = 0.1


def lambda_handler(event, context):
    try:
        sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        order_id = sns_message['order_id']
        result = sns_message['result']

        utils.log("PAYMENT_P2", {'order_id': order_id, 'result': result})

        return {
            'statusCode': 200,
            'body': "Payment completed"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


def make_reservation():
    return random.random() >= error_rate
