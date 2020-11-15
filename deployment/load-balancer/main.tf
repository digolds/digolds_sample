terraform {
  required_version = "= 0.12.19"
}

provider "aws" {
  version = "= 2.58"
  region = "ap-northeast-1"
}

data "terraform_remote_state" "dynamodb" {
  backend = "local"

  config = {
    path = "../nosql/terraform.tfstate"
  }
}

locals {
  table_name = format("TABLE_NAME=%s", data.terraform_remote_state.dynamodb.outputs.dynamodb_instance.name)
  index_name = format("INDEX_NAME=%s", tolist(data.terraform_remote_state.dynamodb.outputs.dynamodb_instance.global_secondary_index)[0].name)
}

module "load_balance" {
  source       = "github.com/2cloudlab/module_load_balancer//modules/load_balancer?ref=v0.0.1"
  download_url = "https://github.com/digolds/digolds_sample/archive/v0.0.1.tar.gz"
  package_base_dir         = "digolds_sample-0.0.1"
  app_dir = "personal-blog"
  envs     = ["USER_NAME=slz", "PASSWORD=abc", local.table_name, local.index_name]
  wsgi_app = "wsgiapp:wsgi_app"
}

output "alb_dns_name" {
  value       = module.load_balance.alb_dns_name
  description = "The domain name of the load balancer"
}