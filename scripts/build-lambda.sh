#!/usr/bin/env bash
# Bundles the API for AWS Lambda into api/dist-lambda: the app plus its
# dependencies, built for Lambda's Linux runtime (so it works from macOS too).
# Terraform zips that folder at apply time.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
out="$root/api/dist-lambda"

rm -rf "$out"
mkdir -p "$out"

python3 -m pip install \
  --requirement "$root/api/requirements-lambda.txt" \
  --target "$out" \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.13 \
  --only-binary=:all: \
  --quiet \
  --disable-pip-version-check

cp -R "$root/api/app" "$out/app"
find "$out" -name "__pycache__" -type d -prune -exec rm -rf {} +

echo "Lambda bundle written to api/dist-lambda"
