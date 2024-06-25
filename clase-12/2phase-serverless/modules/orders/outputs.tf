output "orders_update_destination" {
  value = aws_sqs_queue.order_update.arn
}

output "phase_1_sns" {
  value = aws_sns_topic.order_request_p1.arn
}

output "phase_2_sns" {
  value = aws_sns_topic.order_update_p2.arn
}
