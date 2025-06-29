#!/bin/bash

echo "Arrêt et suppression complète de l'environnement DEV PTS + volumes..."

docker-compose \
  -f compose/docker-compose.pts.base.yml \
  -f compose/docker-compose.pts.dev.yml \
  down -v --remove-orphans

echo "Volumes supprimés, environnement local propre."
