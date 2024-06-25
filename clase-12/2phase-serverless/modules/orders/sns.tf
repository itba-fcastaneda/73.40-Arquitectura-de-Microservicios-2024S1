resource "aws_sns_topic" "order_request_p1" {
  name = "OrderRequest_P1"
}

resource "aws_sns_topic" "order_update_p2" {
  name = "OrderUpdate_P2"
}

resource "aws_sns_topic_subscription" "phase_1_suscriptions" {

  for_each = var.phase_1_suscriptors

  topic_arn = aws_sns_topic.order_request_p1.arn
  protocol  = "lambda"
  endpoint  = each.value
}

resource "aws_sns_topic_subscription" "phase_2_suscriptions" {

  for_each = var.phase_2_suscriptors

  topic_arn = aws_sns_topic.order_update_p2.arn
  protocol  = "lambda"
  endpoint  = each.value
}
