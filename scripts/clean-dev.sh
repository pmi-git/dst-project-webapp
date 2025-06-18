#!/bin/bash

echo "Arrêt et suppression complète de l'environnement DEV + volumes..."

docker-compose \
  -f compose/docker-compose.base.yml \
  -f compose/docker-compose.dev.yml \
  down -v --remove-orphans

echo "Volumes supprimés, environnement local propre."
