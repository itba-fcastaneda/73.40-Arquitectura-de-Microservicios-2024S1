resource "aws_lambda_function" "this" {

  filename      = var.filename
  function_name = var.function_name
  role          = "arn:aws:iam::${var.account_id}:role/LabRole"
  handler       = var.handler
  runtime       = var.runtime

  source_code_hash = filebase64sha256(var.filename)

  tags = {
    name = "${var.function_name}"
  }

  timeout = 5 # Timeout in seconds
  lifecycle {
    create_before_destroy = true
  }

  environment {
    variables = var.env_vars
  }

  layers = var.layers
}
