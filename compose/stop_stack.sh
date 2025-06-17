#!/bin/bash

echo "🛑 Arrêt propre des conteneurs Docker..."
docker-compose -f docker-compose.base.yml down -v

echo "🧹 Nettoyage terminé."
