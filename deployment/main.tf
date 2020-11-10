terraform {
  required_version = "= 0.12.19"
}

provider "aws" {
  version = "= 2.58"
  region  = "ap-northeast-1"
}

module "dynamodb" {
  source       = "github.com/2cloudlab/module_dynamodb//modules/dynamodb?ref=v0.0.1"
  name         = "personal-articles-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "Id"
  attributes = [
    {
      name = "Id"
      type = "N"
    },
    {
      name = "ContentType"
      type = "N"
    },
    {
      name = "CreatedDateTime"
      type = "N"
  }, ]
  global_secondary_indexes = [{
    name               = "ContentGlobalIndex"
    hash_key           = "ContentType"
    range_key          = "CreatedDateTime"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["Id", "Title", "Description", "AuthorName"]
  }, ]
}

output "dynamodb_instance" {
  value = module.dynamodb.dynamodb_instance
}