#!/usr/bin/env bash

set -euo pipefail

helm dependency update servarr
 
for chart in servarr/charts/*/; do
  if [ -f "$chart/Chart.yaml" ]; then
    echo helm lint "$chart"
  fi
done