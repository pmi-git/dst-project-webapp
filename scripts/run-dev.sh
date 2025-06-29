#!/bin/bash

echo "Lancement de l’environnement DEV WordPress..."
./scripts/run-wp-dev.sh || { echo "Échec du lancement WordPress"; exit 1; }

echo "Lancement de l’environnement DEV PrestaShop..."
./scripts/run-pts-dev.sh || { echo "Échec du lancement PrestaShop"; exit 1; }

echo "Les deux environnements DEV sont lancés avec succès."
