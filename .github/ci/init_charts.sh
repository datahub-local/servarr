#!/usr/bin/env bash

set -euo pipefail

helm dependency update servarr
 
for chart in servarr/charts/*/; do
  if [ -f "$chart/Chart.yaml" ]; then
    helm dependency update "$chart"
  fi
done