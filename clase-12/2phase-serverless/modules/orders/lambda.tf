module "orderUpdate" {
  source = "..\/lambda"


  account_id    = var.account_id
  service_name  = "orders"
  function_name = "orderUpdate"

  filename = "./lambda_src/orders/orderUpdate.zip"
  handler  = "lambda_function.lambda_handler"
  runtime  = "python3.12"
  env_vars = {
    "ORDERS_TOPIC_ARN"         = aws_sns_topic.order_request_p1.arn
    "SECOND_PHASE_TOPIC_ARN"   = aws_sns_topic.order_update_p2.arn
    "ORDERS_DYNAMO_TABLE_NAME" = aws_dynamodb_table.orders.name
  }
  layers = [var.utils_layer]

}

module "orderPlacement" {
  source = "..\/lambda"


  account_id    = var.account_id
  service_name  = "orders"
  function_name = "placeOrder"

  filename = "./lambda_src/orders/placeOrder.zip"
  handler  = "lambda_function.lambda_handler"
  runtime  = "python3.12"
  env_vars = {
    "ORDERS_TOPIC_ARN"         = aws_sns_topic.order_request_p1.arn
    "SECOND_PHASE_TOPIC_ARN"   = aws_sns_topic.order_update_p2.arn
    "ORDERS_DYNAMO_TABLE_NAME" = aws_dynamodb_table.orders.name
  }
  layers = [var.utils_layer]

}

resource "aws_lambda_event_source_mapping" "order_update_origin" {
  event_source_arn = aws_sqs_queue.order_update.arn
  function_name    = module.orderUpdate.function_arn
}
