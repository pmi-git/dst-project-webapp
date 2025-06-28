#!/bin/bash

echo "Arrêt des conteneurs et suppression des volumes..."
docker-compose -f docker-compose.wp.base.yml down -v

echo "Reconstruction complète des images..."
docker-compose -f docker-compose.wp.base.yml build --no-cache

echo "Lancement des conteneurs en arrière-plan..."
docker-compose -f docker-compose.wp.base.yml up -d

echo "Environnement relancé avec succès."
