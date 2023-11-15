# Lambda IAM Role
########################################

resource "aws_iam_role" "reporting_lambda_role" {
  name = "reporting-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "sts:AssumeRole"
        ]
        Effect = "Allow",
        Principal = {
          Service = [
            "lambda.amazonaws.com"
          ]
        }
      }
    ]
  })

  tags = merge({ "Name" : "reporting-lambda-role" }, var.tag_all)
}

resource "aws_iam_policy" "reporting_lambda_iam_policy" {
  name        = "reporting-lambda-policy"
  path        = "/"
  description = "Policy for the reporting lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject"
        ]
        Effect  = "Allow"
        Resouce = "${aws_s3_bucket.reporting_bucket.arn}/*"
      }
    ]
  })
}
