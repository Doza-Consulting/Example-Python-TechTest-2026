output "site_url" {
  description = "Public URL of the deployed app (UI at /, API at /api)."
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "ui_bucket" {
  description = "S3 bucket the built UI is uploaded to."
  value       = aws_s3_bucket.ui.bucket
}

output "cloudfront_distribution_id" {
  description = "Used to invalidate the CDN cache after a UI deploy."
  value       = aws_cloudfront_distribution.main.id
}
