# Terraform

Deploys the app to AWS using the cheapest, simplest services:

| Piece | Service |
|---|---|
| UI | private S3 bucket behind CloudFront |
| API | Lambda (Python 3.13) exposed via a Function URL; CloudFront routes `/api/*` to it |
| Data | DynamoDB, one on-demand table each for rooms, game masters and bookings |

Everything is pay-per-use, so idle cost is close to zero. The UI and API share
one CloudFront domain, so no CORS configuration is needed.

## Folder structure

```
terraform/
├── versions.tf     Terraform + provider versions, AWS provider and default tags
├── variables.tf    region, project name, environment, Lambda bundle path
├── main.tf         shared naming (`<project>-<environment>`)
├── dynamodb.tf     the three DynamoDB tables
├── lambda.tf       API Lambda, IAM role/policies, public Function URL
├── frontend.tf     S3 bucket, CloudFront distribution (UI at /, API at /api/*)
└── outputs.tf      site URL, bucket name, distribution ID
```

## How the pieces fit together

- Browser → CloudFront. Requests to `/api/*` go to the Lambda Function URL
  with caching off. Everything else is served from the private S3 bucket.
- The Lambda runs the same FastAPI app as local dev (`api/app/lambda_handler.py`, via Mangum),
  with `STORAGE=dynamodb`, and strips the `/api` prefix before routing.
- The Lambda's IAM role can only read/write the three tables and write logs.
- The S3 bucket blocks public access; only this CloudFront distribution can read it.
- The Lambda code comes from `api/dist-lambda`, zipped by Terraform at apply
  time. If you skip `make build-lambda`, `apply` fails because that folder
  doesn't exist.

## Prerequisites

- Terraform >= 1.5, AWS CLI, Python 3.12+ and Node 22.13+
- AWS credentials configured (`aws configure` or `AWS_PROFILE`) with permission
  to create the resources above

## Deploy

From the repo root:

```bash
make install
make build-lambda                         # bundles the API to api/dist-lambda
terraform -chdir=terraform init
terraform -chdir=terraform apply
./scripts/deploy-ui.sh                    # builds UI, uploads to S3, invalidates CDN
```

`terraform apply` prints `site_url`. The UI is at `/`, the API at `/api`
(e.g. `<site_url>/api/health`). Re-run the `build-lambda` + `apply` steps after
API changes, and `deploy-ui.sh` after UI changes.

Rooms and game masters are seeded into DynamoDB the first time the API runs.

## Variables

See `variables.tf`: `aws_region` (default `eu-west-2`), `project_name`,
`environment`. Override with `-var` or a `terraform.tfvars` file (git-ignored).

## Tear down

```bash
terraform -chdir=terraform destroy
```

## Good to know

- State is stored locally by default. Don't commit `*.tfstate`. For a shared
  environment, add an S3 backend in `versions.tf`.
- The Lambda Function URL is public (no IAM auth), which keeps it cheap and
  simple but means it can be called directly as well as through CloudFront.
- The UI uses hash routing, so CloudFront needs no SPA error-page fallback
  (which would also rewrite the API's 404 responses).
- Useful checks: `terraform fmt`, `terraform validate`, `terraform plan`.
- Terraform creates real, billable AWS resources. Run `terraform destroy` when
  you're finished.
