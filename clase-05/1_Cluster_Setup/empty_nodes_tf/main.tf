provider "aws" {
  region = local.region
}

resource "aws_key_pair" "node-key" {
  key_name   = "cluster-keypair"
  public_key = file(local.key_file_name)
}

resource "aws_instance" "master" {
  ami                    = local.ami
  instance_type          = local.instance_type
  key_name               = aws_key_pair.node-key.key_name
  vpc_security_group_ids = [aws_security_group.example.id]

  tags = {
    Name = "master-node"
  }
}

resource "aws_instance" "node" {
  count                  = 2
  ami                    = local.ami
  instance_type          = local.instance_type
  key_name               = aws_key_pair.node-key.key_name
  vpc_security_group_ids = [aws_security_group.example.id]

  tags = {
    Name = "worker-node-${count.index + 1}"
  }
}

resource "aws_security_group" "example" {
  name        = "example-security-group"
  description = "Allow all inbound and outbound traffic"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "ssh_commands_to_worker_nodes" {
  value       = [for public_dns in aws_instance.node.*.public_dns : "ssh ubuntu@${public_dns}"]
  description = "SSH commands to connect to Kubernetes worker nodes"
}

output "ssh_commands_to_master_node" {
  value       = "ssh ubuntu@${aws_instance.master.public_dns}"
  description = "SSH commands to connect to Kubernetes master node"
}
