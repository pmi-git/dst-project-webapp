#!/bin/bash

echo "Suivi des logs en temps réel pour l'environnement DEV WP..."

docker-compose \
  -f compose/docker-compose.wp.base.yml \
  -f compose/docker-compose.wp.dev.yml \
  logs -f --tail=50
