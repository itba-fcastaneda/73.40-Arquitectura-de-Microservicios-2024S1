variable "service_name" {
  type        = string
  description = "Service name used as prefix for resources' names."
}

variable "account_id" {
  type = string
}

variable "lambda_phase_1" {
  type = object({
    filename = string
    handler  = string
    runtime  = string
    env_vars = map(string)
    layers   = list(string)
  })
  description = "Lambda needed variables: filename, handler, runtime, env_vars and layers."
}

variable "lambda_phase_2" {
  type = object({
    filename = string
    handler  = string
    runtime  = string
    env_vars = map(string)
    layers   = list(string)
  })
  description = "Lambda needed variables: filename, handler, runtime, env_vars and layers."
}

variable "phase_1_destination_arn" {
  type = string
}

variable "phase_1_sns" {
  type = string
}

variable "phase_2_sns" {
  type = string
}
