
module "utils_layer" {
  source = "modules\/utils_layer"

  filename = "./lambda_src/utils_layer/python.zip"
}

module "orders_service" {
  source = "modules\/orders"

  account_id  = data.aws_caller_identity.current.account_id
  utils_layer = module.utils_layer.layer_arn

  phase_1_suscriptors = {
    inventory : module.service["inventory"].phase_1_lambda_arn
    payment : module.service["payment"].phase_1_lambda_arn
    shipping : module.service["shipping"].phase_1_lambda_arn
  }
  phase_2_suscriptors = {
    inventory : module.service["inventory"].phase_2_lambda_arn
    payment : module.service["payment"].phase_2_lambda_arn
    shipping : module.service["shipping"].phase_2_lambda_arn
  }
}

module "service" {
  for_each = local.services

  source     = "modulestwo_phase_suscriptor"
  account_id = data.aws_caller_identity.current.account_id

  service_name = each.value.name

  lambda_phase_1 = each.value.lambda_phase_1
  lambda_phase_2 = each.value.lambda_phase_2
  phase_1_sns    = module.orders_service.phase_1_sns
  phase_2_sns    = module.orders_service.phase_2_sns

  phase_1_destination_arn = module.orders_service.orders_update_destination

}
