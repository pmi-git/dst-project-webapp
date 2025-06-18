#!/bin/bash

echo "🔄 Arrêt des conteneurs existants (dev)..."
docker-compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml down -v

echo "🔨 Reconstruction des images (dev)..."
docker-compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml build --no-cache

echo "🚀 Lancement de l'environnement DEV (SSL sur https://localhost:8443)..."
docker-compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml up -d

echo "✅ WordPress DEV lancé. Accès : https://localhost:8443"
