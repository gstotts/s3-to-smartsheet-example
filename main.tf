terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "gregorystotts-dot-com"

    workspaces {
      name = "lambda-example"
    }
  }

  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.25.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}
