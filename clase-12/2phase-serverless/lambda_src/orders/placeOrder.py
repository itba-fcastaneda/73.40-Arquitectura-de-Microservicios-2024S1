import utils


def lambda_handler(event, context):
    try:

        order_info = {
            'customer_name': 'John Doe',
            'product_id': '12345',
            'quantity': 2,
            'total_amount': 50,
            'order_date': '2024-06-07'
        }

        order_id = utils.create(order_info)

        utils.log("PLACE_ORDER", {'order_id': order_id})

        utils.notify_new_order(order_id, order_info)

        return {
            'statusCode': 200,
            'body': 'Published message to SNS'
        }
    except Exception as e:
        print("ORDERS", "Error publishing message to SNS topic:", e)
        return {
            'statusCode': 500,
            'body': 'Error publishing order placement to SNS topic: {}'.format(e)
        }
