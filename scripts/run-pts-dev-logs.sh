#!/bin/bash

echo "Suivi des logs en temps réel pour l'environnement DEV PTS ..."

docker-compose \
  -f compose/docker-compose.pts.base.yml \
  -f compose/docker-compose.pts.dev.yml \
  logs -f --tail=50
