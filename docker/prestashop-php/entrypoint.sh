#!/bin/bash
set -e

echo "PrestaShop - Entrypoint initialisé"

DB_HOST="$PTS_DB_HOST"
DB_PORT="3306"

# Attente de la base de données
echo "Attente de MariaDB sur ${DB_HOST}:${DB_PORT}..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo -e "\nBase de données prête !"

# Si installation auto activée
if [[ "$PS_INSTALL_AUTO" == "1" ]]; then
  echo "Installation automatique de PrestaShop (si non déjà installée)..."
  if [[ ! -f ./config/settings.inc.php ]]; then
    echo "Démarrage du script d'install CLI..."

    php install/index_cli.php \
      --language=fr \
      --country=fr \
      --domain=localhost:8444 \
      --db_server="$DB_HOST" \
      --db_name="$PTS_DB_NAME" \
      --db_user="$PTS_DB_USER" \
      --db_password="$PTS_DB_PASSWORD" \
      --prefix=ps_ \
      --email="admin@prestashop.dev" \
      --password="admin" \
      --name="Boutique Dev" || echo "Installation échouée (peut-être déjà faite ?)"
  else
    echo "PrestaShop semble déjà installé (config/settings.inc.php présent)"
  fi
else
  echo "PS_INSTALL_AUTO non activé, on ne fait rien"
fi

echo "Lancement de PHP-FPM..."
exec php-fpm
