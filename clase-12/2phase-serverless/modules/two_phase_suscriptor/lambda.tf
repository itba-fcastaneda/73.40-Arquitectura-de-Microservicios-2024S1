
module "lambda_phase_message_handlers" {

  for_each = {
    phase_1 = var.lambda_phase_1,
    phase_2 = var.lambda_phase_2
  }

  source = "..\/lambda"

  account_id    = var.account_id
  service_name  = var.service_name
  function_name = "${var.service_name}_${each.key}"

  filename = each.value.filename
  runtime  = each.value.runtime
  handler  = each.value.handler
  env_vars = each.value.env_vars
  layers   = each.value.layers
}

resource "aws_lambda_permission" "phase_1" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_phase_message_handlers["phase_1"].function_arn
  principal     = "sns.amazonaws.com"
  source_arn    = var.phase_1_sns
}

resource "aws_lambda_permission" "phase_2" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_phase_message_handlers["phase_2"].function_arn
  principal     = "sns.amazonaws.com"
  source_arn    = var.phase_2_sns
}

resource "aws_lambda_function_event_invoke_config" "phase_1_destination" {
  function_name = module.lambda_phase_message_handlers["phase_1"].function_arn

  destination_config {
    on_success {
      destination = var.phase_1_destination_arn
    }
  }
}
