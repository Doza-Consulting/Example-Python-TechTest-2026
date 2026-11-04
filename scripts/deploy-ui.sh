#!/usr/bin/env bash
# Builds the UI, uploads it to the S3 bucket created by Terraform and
# invalidates the CloudFront cache. Run `terraform apply` first.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"

bucket="$(terraform -chdir="$root/terraform" output -raw ui_bucket)"
dist_id="$(terraform -chdir="$root/terraform" output -raw cloudfront_distribution_id)"

npm run build -w ui --prefix "$root"
aws s3 sync "$root/ui/dist" "s3://$bucket" --delete
aws cloudfront create-invalidation --distribution-id "$dist_id" --paths "/*" >/dev/null

echo "Deployed: $(terraform -chdir="$root/terraform" output -raw site_url)"
