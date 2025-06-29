#!/bin/bash

echo "État de l’environnement DEV PTS (containers + health)..."
echo ""

docker-compose \
  -f compose/docker-compose.pts.base.yml \
  -f compose/docker-compose.pts.dev.yml \
  ps --services --filter "status=running"

echo ""
echo "Vérification des statuts de santé :"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "pts-nginx|pts-php|pts-mysql|pts-redis"
