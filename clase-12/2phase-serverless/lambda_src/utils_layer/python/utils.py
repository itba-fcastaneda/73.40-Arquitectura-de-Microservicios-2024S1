import json
import os
import uuid

import boto3

sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

ORDERS_TOPIC_ARN = os.getenv('ORDERS_TOPIC_ARN')
SECOND_PHASE_TOPIC_ARN = os.getenv('SECOND_PHASE_TOPIC_ARN')
ORDERS_DYNAMO_TABLE_NAME = os.getenv('ORDERS_DYNAMO_TABLE_NAME')

def publish_to_sns(topic_arn, message):
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    return response


def commit(order_id):
    return publish_to_sns(SECOND_PHASE_TOPIC_ARN, {'order_id': order_id, 'result': 'COMMIT'})


def rollback(order_id):
    return publish_to_sns(SECOND_PHASE_TOPIC_ARN, {'order_id': order_id, 'result': 'ROLLBACK'})


def notify_new_order(order_id, order_info):
    return publish_to_sns(ORDERS_TOPIC_ARN, {
        'order_id': order_id,
        'order_info': order_info
    })


def update(order_id, service, status):
    orders_table = dynamodb.Table(ORDERS_DYNAMO_TABLE_NAME)
    update_expression = f'SET #service_alias = :status'
    expression_attribute_names = {'#service_alias': service}
    expression_attribute_values = {':status': status}

    orders_table.update_item(
        Key={'id': order_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )


def get(order_id):
    orders_table = dynamodb.Table(ORDERS_DYNAMO_TABLE_NAME)
    response = orders_table.get_item(Key={'id': order_id})
    return response.get('Item')


def create(order_info):
    orders_table = dynamodb.Table(ORDERS_DYNAMO_TABLE_NAME)
    order_id = str(uuid.uuid4())

    order_object = {
        **order_info,
        'inventory': 'on_hold',
        'payment': 'on_hold',
        'shipping': 'on_hold'
    }

    orders_table.put_item(Item={'id': order_id, **order_object})

    return order_id


def is_ready(order_id):
    order = get(order_id)
    return all([order.get('inventory') == 'accepted',
                order.get('payment') == 'accepted',
                order.get('shipping') == 'accepted'])


def log(subject, body):
    result = subject
    for key, value in body.items():
        result += f" {key}: {value}"

    print(result)
