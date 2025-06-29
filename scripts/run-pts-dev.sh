#!/bin/bash

CERT_DIR="./ssl"
CRT_FILE="$CERT_DIR/self-signed.crt"
KEY_FILE="$CERT_DIR/self-signed.key"

# Vérification des certificats SSL
if [ ! -f "$CRT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  echo "Certificat SSL manquant, génération automatique..."
  ./scripts/generate-cert.sh
else
  echo "Certificat SSL déjà présent."
fi

echo "Arrêt des conteneurs existants (dev pts)..."
docker-compose -f compose/docker-compose.pts.base.yml -f compose/docker-compose.pts.dev.yml down -v

echo "Reconstruction des images (dev pts)..."
docker-compose -f compose/docker-compose.pts.base.yml -f compose/docker-compose.pts.dev.yml build --no-cache

echo "Lancement de l'environnement DEV PTS (SSL sur https://localhost:8444)..."
docker-compose -f compose/docker-compose.pts.base.yml -f compose/docker-compose.pts.dev.yml up -d

echo "Prestashop DEV lancé. Accès : https://localhost:8444"
