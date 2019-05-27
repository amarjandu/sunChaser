data "aws_caller_identity" "current" {}


resource aws_s3_bucket upload_bucket {
  count = "${length(var.UPLOAD_BUCKET) > 0 ? 1 : 0}"
  bucket = "${var.UPLOAD_BUCKET}"

}
