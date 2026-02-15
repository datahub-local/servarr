#!/usr/bin/env bash

set -euo pipefail

CURRENT_DIR="$(dirname "$(realpath "$0")")"

NAMESPACE="servarr"

"$CURRENT_DIR/init_charts.sh"

helm upgrade --install --create-namespace --namespace "$NAMESPACE" \
  --values $CURRENT_DIR/ci-values.yaml servarr servarr
