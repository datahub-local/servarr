#!/usr/bin/env bash

set -euo pipefail

helm repo add datahub-local https://datahub-local.github.io/servarr/

for chart in charts/*/; do
  if [ -f "$chart/Chart.yaml" ]; then
    helm dependency update "$chart"
  fi
done