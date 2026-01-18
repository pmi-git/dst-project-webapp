#!/usr/bin/env bash
set -euo pipefail

minikube status >/dev/null 2>&1 || minikube start

# Ingress NGINX via Helm (portable)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx >/dev/null 2>&1 || true
helm repo update

kubectl get ns ingress-nginx >/dev/null 2>&1 || kubectl create ns ingress-nginx

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  -n ingress-nginx

echo "Minikube IP: $(minikube ip)"
echo "Add to /etc/hosts:"
echo "$(minikube ip)  wp.dev.local"
echo "$(minikube ip)  pts.dev.local"
