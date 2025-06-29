#!/bin/bash

echo "État de l’environnement DEV WordPress :"
./scripts/status-wp-dev.sh || echo "WordPress indisponible"

echo ""
echo "État de l’environnement DEV PrestaShop :"
./scripts/status-pts-dev.sh || echo "PrestaShop indisponible"

echo ""
echo "Vérification des deux environnements terminée."
