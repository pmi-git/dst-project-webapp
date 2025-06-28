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

echo "Arrêt des conteneurs existants (dev)..."
docker-compose -f compose/docker-compose.wp.base.yml -f compose/docker-compose.wp.dev.yml down -v

echo "Reconstruction des images (dev)..."
docker-compose -f compose/docker-compose.wp.base.yml -f compose/docker-compose.wp.dev.yml build --no-cache

echo "Lancement de l'environnement DEV (SSL sur https://localhost:8443)..."
docker-compose -f compose/docker-compose.wp.base.yml -f compose/docker-compose.wp.dev.yml up -d

echo "WordPress DEV lancé. Accès : https://localhost:8443"
