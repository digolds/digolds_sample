terraform {
  required_version = "= 0.12.19"
}

provider "aws" {
    version = "= 2.58"
    region = "ap-northeast-1"
}

data "template_file" "shell" {
  template = file("${path.module}/service.sh")
}

resource "aws_instance" "virtual_machine" {
  ami           = "ami-06a46da680048c8ae"
  instance_type = "t2.micro"
  user_data = base64encode(data.template_file.shell.rendered)
  security_groups = [aws_security_group.sg1.name]
  key_name = "for_you"
}

resource "aws_security_group" "sg1" {
  name        = "allow_http_traffic"
  description = "Allow http traffic"

  ingress {
    description = "All http traffics from Internet"
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

output "vm_info" {
    value = {
      ip = aws_instance.virtual_machine.public_ip
      cpu = aws_instance.virtual_machine.cpu_core_count
      instance_type = aws_instance.virtual_machine.instance_type
      root_block_device = aws_instance.virtual_machine.root_block_device
    }
}