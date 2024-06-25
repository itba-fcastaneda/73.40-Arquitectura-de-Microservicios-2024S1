resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = var.filename
  layer_name = "utils_layers"

  compatible_runtimes = ["python3.12"]

  source_code_hash = filebase64sha256(var.filename)
}
