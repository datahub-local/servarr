#!/usr/bin/env bash

set -euo pipefail

NAMESPACE="servarr"

echo "=== Waiting for all pods to be ready ==="
kubectl wait --for=condition=Ready pod \
  -l "app.kubernetes.io/instance=servarr" \
  -n "$NAMESPACE" \
  --timeout=600s --field-selector=status.phase!=Succeeded,status.phase!=Failed || {
    echo "ERROR: Pods did not become ready in time"
    
    echo "=== Pod descriptions ==="
    kubectl describe pods -n "$NAMESPACE" -l "app.kubernetes.io/instance=servarr"
    
    echo "=== Pod logs ==="
    for pod in $(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/instance=servarr" -o jsonpath='{.items[*].metadata.name}'); do
      echo "--- Logs from pod: $pod ---"
      kubectl logs "$pod" -n "$NAMESPACE" --all-containers=true || true
    done
    
    exit 1
  }

echo "=== Pod status ==="
kubectl get pods -n "$NAMESPACE" -o wide

echo "=== Waiting for init jobs to complete ==="
ret=0
for job in $(kubectl get jobs -n "$NAMESPACE" -o jsonpath='{.items[*].metadata.name}'); do
  echo "Waiting for job: $job"
  kubectl wait --for=condition=Complete "job/$job" -n "$NAMESPACE" --timeout=600s || {
    echo "ERROR: Job $job did not complete"

    echo "=== Job status ==="
    kubectl get jobs -n "$NAMESPACE" $job
    
    echo "=== Pod descriptions ==="
    kubectl describe "job/$job" -n "$NAMESPACE"
    
    echo "=== Pod logs ==="
    kubectl logs "job/$job" -n "$NAMESPACE" --all-containers=true || true
    
    exit 1
  }
done

if [ $ret -ne 0 ]; then
  exit $ret
fi

echo "[✓] All tests passed!"
