output "phase_1_lambda_arn" {
  value = module.lambda_phase_message_handlers["phase_1"].function_arn
}

output "phase_2_lambda_arn" {
  value = module.lambda_phase_message_handlers["phase_2"].function_arn
}
