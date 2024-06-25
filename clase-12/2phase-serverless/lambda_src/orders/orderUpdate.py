import json

import utils


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message = json.loads(record['body'])
            data = json.loads(message.get('responsePayload').get('body'))
            status = data.get('status')

            order_id = data.get('orderId')
            service = data.get('service')

            utils.log("UPDATE", {"order_id": order_id, "service": service, "status": status})

            utils.update(order_id, service, status)

            if status == 'rejected':
                utils.log("ROLLBACK", {"order_id": order_id})
                utils.rollback(order_id)
            elif utils.is_ready(order_id):
                utils.log("COMMIT", {"order_id": order_id})
                utils.commit(order_id)

        return {
            'statusCode': 200
        }
    except Exception as e:
        print("ORDERS", "Error updating order status:", e)
        return {
            'statusCode': 500,
            'body': 'Error updating order status: {}'.format(e)
        }
