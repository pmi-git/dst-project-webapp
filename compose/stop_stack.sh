#!/bin/bash

echo "🛑 Arrêt propre des conteneurs Docker..."
docker-compose -f compose/docker-compose.base.yml down

echo "🧹 Nettoyage terminé."
