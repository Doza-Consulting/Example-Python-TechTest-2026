# Scripts

Helper scripts for working with the repo.

| Script | Purpose |
|---|---|
| `build-lambda.sh` | Bundles the API and its dependencies for AWS Lambda into `api/dist-lambda` (`make build-lambda`) |
| `deploy-ui.sh` | Builds the UI, uploads it to the S3 bucket created by Terraform and invalidates the CloudFront cache |

## deploy-ui.sh

```bash
./scripts/deploy-ui.sh
```

Prerequisites:

- `terraform apply` has already been run (the script reads the bucket name and
  CloudFront distribution ID from Terraform outputs)
- AWS CLI installed with credentials configured for the same account/region
- dependencies installed (`make install`)

It prints the site URL when it finishes. See [../terraform/README.md](../terraform/README.md)
for the full deployment steps.
