#!/bin/bash

set -e

echo "⏳ Attente de MySQL ($WORDPRESS_DB_HOST)..."

export MYSQL_PWD="$WORDPRESS_DB_PASSWORD"
until mysql \
  --ssl=0 \
  -h"$WORDPRESS_DB_HOST" \
  -u"$WORDPRESS_DB_USER" \
  -e "SELECT 1" "$WORDPRESS_DB_NAME" >/dev/null 2>&1; do
  sleep 2
done

echo "✅ MySQL disponible"

# Vérifier si WP est installé
if wp core is-installed --allow-root; then
  echo "✅ WordPress installé — activation Redis"
  wp plugin activate redis-cache --allow-root || true
  wp redis enable --allow-root || true
else
  echo "ℹ️ WordPress non installé — rien à activer"
fi

echo "🚀 PHP-FPM prêt"
exec php-fpm -F
