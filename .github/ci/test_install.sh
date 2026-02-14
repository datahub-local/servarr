#!/usr/bin/env bash

set -euo pipefail

NAMESPACE="servarr"

helm upgrade --install --dependency-update --create-namespace --namespace "$NAMESPACE" \
  --values .github/ci/ci-values.yaml servarr servarr
