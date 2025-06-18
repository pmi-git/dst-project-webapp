#!/bin/bash

echo "Suivi des logs en temps réel pour l'environnement DEV..."

docker-compose \
  -f compose/docker-compose.base.yml \
  -f compose/docker-compose.dev.yml \
  logs -f --tail=50
