# Lambda Example
#
# This lambda is triggered when an object
# is added to the reporting S3 bucket.
########################################

resource "aws_lambda_function" "file_drop_lambda" {
  function_name = "reporting-lambda"

  filename         = "${path.module}/functions/report_to_smartsheet/ReportToSmartsheet.zip"
  role             = aws_iam_role.reporting_lambda_role.arn
  handler          = "ReportToSmartsheet.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256("${path.module}/functions/report_to_smartsheet/ReportToSmartsheet.zip")
  layers           = [aws_lambda_layer_version.aws_lambda_layer_version.smartsheet_lambda_layer.arn]

  tags = merge({ "Name" : "reporting-lambda" }, var.tag_all)
}

resource "aws_lambda_permission" "allow_s3_invoke_lambda" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.file_drop_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.reporting_bucket.arn
}

resource "aws_lambda_layer_version" "smartsheet_lambda_layer" {
  filename   = "${path.module}/functions/report_to_smartsheet/smartsheet.zip"
  layer_name = "smartsheet_sdk"

  compatible_runtimes = ["python3.11"]
}