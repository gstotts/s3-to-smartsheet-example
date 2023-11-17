data "aws_caller_identity" "current" {}

data "aws_secretsmanager_secret" "smar_token" {
    name = "smar_token"
}

data "aws_secretsmanager_secret_version" "smar_access_token" {
  secret_id = data.aws_secretsmanager_secret.smar_token.id
}

locals {
  account_id = data.aws_caller_identity.current.account_id
}
