variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Prefix for resource names."
  type        = string
  default     = "escapequeue"
}

variable "environment" {
  description = "Environment name, e.g. dev."
  type        = string
  default     = "dev"
}

variable "lambda_bundle_dir" {
  description = "Directory containing the bundled Lambda (output of `make build-lambda`)."
  type        = string
  default     = "../api/dist-lambda"
}
