#!/bin/bash

echo "Nettoyage de l’environnement DEV WordPress..."
./scripts/clean-wp-dev.sh || echo "Échec du nettoyage WordPress"

echo "Nettoyage de l’environnement DEV PrestaShop..."
./scripts/clean-pts-dev.sh || echo "Échec du nettoyage PrestaShop"

echo "Nettoyage complet terminé."
