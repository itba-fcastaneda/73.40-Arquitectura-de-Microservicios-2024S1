import json
import random
import utils

service = 'inventory'
error_rate = 0.1


def lambda_handler(event, context):
    try:
        sns_message = json.loads(event['Records'][0]['Sns']['Message'])
        order_id = sns_message['order_id']
        order_info = sns_message['order_info']

        status = 'accepted' if make_reservation() else 'rejected'

        message = {
            'status': status,
            'orderId': order_id,
            'service': service
        }

        utils.log('INVENTORY_P1', {'order_id': order_id, 'status': status})

        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


def make_reservation():
    return random.random() >= error_rate
