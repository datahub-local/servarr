#!/usr/bin/env bash

set -uo pipefail

NAMESPACE="servarr"

echo "=== All pods ==="
kubectl get pods -n "$NAMESPACE" -o wide

echo "=== Pod descriptions ==="
kubectl describe pods -n "$NAMESPACE"

echo "=== Events ==="
kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp'

echo "=== Job logs ==="
for job in $(kubectl get jobs -n "$NAMESPACE" -o jsonpath='{.items[*].metadata.name}'); do
  echo "--- Logs for job: $job ---"
  kubectl logs "job/$job" -n "$NAMESPACE" --all-containers=true || true
done

echo "=== Pod logs (last 50 lines each) ==="
for pod in $(kubectl get pods -n "$NAMESPACE" -o jsonpath='{.items[*].metadata.name}'); do
  echo "--- Logs for pod: $pod ---"
  kubectl logs "$pod" -n "$NAMESPACE" --all-containers=true --tail=50 || true
done
