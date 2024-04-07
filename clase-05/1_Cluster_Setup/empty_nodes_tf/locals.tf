locals {
  ami           = "ami-080e1f13689e07408" # Ubuntu 22.04 LTS (HVM), SDD Volume Type
  instance_type = "t2.medium"


  ### ACTUALIZAR ESTOS VALORES
  key_file_name = "~/.ssh/id_rsa.pub"
  region        = "us-east-1"
  ###
}
