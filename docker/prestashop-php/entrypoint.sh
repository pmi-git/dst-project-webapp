#!/bin/bash
set -e

echo "PrestaShop - Entrypoint initialisé"

DB_HOST="${DB_SERVER:-pts-mariadb}"
DB_PORT="${DB_PORT:-3306}"

# Attente de la base de données
echo "Attente de MariaDB sur ${DB_HOST}:${DB_PORT}..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo -n "."
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
      --db_name="${MYSQL_DATABASE:-prestashop}" \
      --db_user="${MYSQL_USER:-prestashop}" \
      --db_password="${MYSQL_PASSWORD:-prestashop}" \
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
