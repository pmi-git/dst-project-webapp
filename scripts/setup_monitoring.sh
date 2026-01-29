#!/bin/bash
# scripts/setup_monitoring.sh
echo "Installation du monitoring..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install monitoring-stack prometheus-community/kube-prometheus-stack -n monitoring
echo "Monitoring installé !"