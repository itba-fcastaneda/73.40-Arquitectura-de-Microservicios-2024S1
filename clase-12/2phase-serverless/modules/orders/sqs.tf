resource "aws_sqs_queue" "order_update" {
  name_prefix = "order_update_from_service"
  fifo_queue  = false

  tags = {
    "service" = "orders"
  }
}
