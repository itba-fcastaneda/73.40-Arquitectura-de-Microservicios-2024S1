variable "filename" {
  description = "The path to the deployment package within the local filesystem."
  type        = string
}

variable "function_name" {
  description = "The name you want to assign to the function."
  type        = string
}

variable "account_id" {
  description = "The AWS account ID that owns the Lambda function."
  type        = string
}

variable "handler" {
  description = "The name of the method within your code that Lambda calls to execute your function."
  type        = string
}

variable "runtime" {
  description = "The runtime environment for the Lambda function you are uploading."
  type        = string
}

variable "service_name" {
  description = "The name of the service."
  type        = string
}

variable "env_vars" {
  description = "A map of string keys and values that are passed as environment variables to the Lambda function."
  type        = map(string)
}

variable "layers" {
  type        = list(string)
  description = "A list of the needed lambda layers versions arns."
}
