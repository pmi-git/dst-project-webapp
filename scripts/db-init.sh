#!/usr/bin/env bash
set -euo pipefail

helm repo add bitnami https://charts.bitnami.com/bitnami >/dev/null 2>&1 || true
helm repo update

kubectl get ns client-wp >/dev/null 2>&1 || kubectl create ns client-wp
kubectl get ns client-pts >/dev/null 2>&1 || kubectl create ns client-pts

# WordPress DB
helm upgrade --install mariadb bitnami/mariadb \
  -n client-wp \
  --set auth.database=wordpress \
  --set auth.username=wpuser \
  --set auth.password=wpPassChangeMe \
  --set auth.rootPassword=rootPassChangeMe \
  --set primary.persistence.enabled=true

# PrestaShop DB
helm upgrade --install mariadb bitnami/mariadb \
  -n client-pts \
  --set auth.database=prestashop \
  --set auth.username=ptsuser \
  --set auth.password=ptsPassChangeMe \
  --set auth.rootPassword=rootPassChangeMe \
  --set primary.persistence.enabled=true
