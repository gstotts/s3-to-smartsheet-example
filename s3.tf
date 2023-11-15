# S3 Bucket For Files To Trigger Lambda
########################################

resource "aws_s3_bucket" "reporting_bucket" {
  bucket = "reporting-${local.account_id}"
  tags   = merge({ "Name" : "reporting-${local.account_id}" }, var.tag_all)
}

resource "aws_s3_bucket_acl" "reporting_acl" {
  bucket = aws_s3_bucket.reporting_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "reporting_versioning" {
  bucket = aws_s3_bucket.reporting_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "reporting_block_public_access" {
  bucket                  = aws_s3_bucket.reporting_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "reporting_lifecycle" {
  bucket = aws_s3_bucket.reporting_bucket.id

  rule {
    id = "remove-noncurrent"

    filter {}

    status = "Enabled"

    noncurrent_version_expiration {
      newer_noncurrent_versions = 14
      noncurrent_days           = 3
    }
  }
}

resource "aws_s3_bucket_notification" "reporting_bucket_notification" {
  bucket = aws_s3_bucket.reporting_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_drop_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke_lambda]
}
