#!/usr/bin/env bash

set -euo pipefail

K3D_CLUSTER_NAME="dev-cluster"
KUBECONFIG_CONTEXT="k3d-${K3D_CLUSTER_NAME}"
export NFS_DIRECTORY=/tmp/k3d_data
export NFS_SERVER=nfs-server

echo "[+] Checking k3d cluster status..."
if ! k3d cluster list "$K3D_CLUSTER_NAME" | grep -q "$K3D_CLUSTER_NAME"; then
  echo "[+] Creating k3d cluster..."
  
  k3d cluster create "$K3D_CLUSTER_NAME" --config .github/ci/k3d-config.yaml
else
  echo "[✓] k3d cluster already exists."
fi

echo "[+] Setting kubectl context to ${KUBECONFIG_CONTEXT}..."
kubectl config use-context "${KUBECONFIG_CONTEXT}" || (echo ERROR && exit 1)

echo "[+] Waiting for Kubernetes to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=60s || (echo ERROR && exit 1)

echo "[+] Start NFS server..."
mkdir -p "$NFS_DIRECTORY"
docker-compose -f .github/ci/nfs-docker-compose.yaml up -d || (echo ERROR && exit 1)

kubectl apply -f .github/ci/nfs-daemonset.yaml

echo "[+] Running helmfile to install charts..."
helmfile apply -f .github/ci/helmfile.yaml.gotmpl || (echo ERROR && exit 1)

# echo "[+] Waiting for pods to be ready..."
# kubectl wait --for=condition=Ready pod -l app=nfs-server-provisioner -n kube-system --timeout=180s || (echo ERROR && exit 1)
# kubectl wait --for=condition=Ready pod -l app=nfs-server-provisioner -n argocd --timeout=180s || (echo ERROR && exit 1)

# echo "[+] Setting up Argo CD port-forward (in background)..."
# pkill -f 'kubectl port-forward svc/argocd-server' || true
# nohup kubectl port-forward svc/argocd-server -n argocd 8080:443 >/dev/null 2>&1 &

# echo "[✓] Argo CD available at https://localhost:8080"