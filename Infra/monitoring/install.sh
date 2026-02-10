#!/bin/bash
# infra/monitoring/install.sh

echo "📦 Installation du monitoring"

# 1. Ajout du repo Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 2. Création du namespace (si pas existe)
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

# 3. Installation avec le fichier de valeurs (qui est dans le même dossier)
# On utilise $(dirname "$0") pour être sûr qu'il trouve le fichier values.yaml à côté du script
helm upgrade --install monitoring-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f "$(dirname "$0")/values.yaml"

echo "✅ Monitoring installé !"