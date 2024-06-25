locals {
  services = {
    inventory = {
      name = "inventory"
      lambda_phase_1 = {
        filename = "./lambda_src/P1/inventory_p1.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }
      lambda_phase_2 = {
        filename = "./lambda_src/P2/inventory_p2.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }
    }

    payment = {
      name = "payment"
      lambda_phase_1 = {
        filename = "./lambda_src/P1/payment_p1.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }

      lambda_phase_2 = {
        filename = "./lambda_src/P2/payment_p2.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }
    }

    shipping = {
      name = "shipping"
      lambda_phase_1 = {
        filename = "./lambda_src/P1/shipping_p1.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }

      lambda_phase_2 = {
        filename = "./lambda_src/P2/shipping_p2.zip"
        handler  = "lambda_function.lambda_handler"
        runtime  = "python3.12"
        env_vars = {}
        layers   = [module.utils_layer.layer_arn]
      }
    }
  }
}
