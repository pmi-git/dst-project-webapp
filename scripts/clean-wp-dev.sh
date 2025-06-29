#!/bin/bash

echo "Arrêt et suppression complète de l'environnement DEV WP + volumes..."

docker-compose \
  -f compose/docker-compose.wp.base.yml \
  -f compose/docker-compose.wp.dev.yml \
  down -v --remove-orphans

echo "Volumes supprimés, environnement local propre."
