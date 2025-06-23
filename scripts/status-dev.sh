#!/bin/bash

echo "État de l’environnement DEV (containers + health)..."
echo ""

docker-compose \
  -f compose/docker-compose.base.yml \
  -f compose/docker-compose.dev.yml \
  ps --services --filter "status=running"

echo ""
echo "Vérification des statuts de santé :"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "nginx|wordpress-php|mysql"
