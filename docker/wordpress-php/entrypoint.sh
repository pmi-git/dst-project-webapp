#!/bin/bash

echo "Lancement de PHP-FPM en arrière-plan..."
php-fpm -D

# Attente de MySQL
until wp db check --allow-root >/dev/null 2>&1; do
  echo "⏳ En attente de la base de données..."
  sleep 2
done

# Si WordPress est installé
if wp core is-installed --allow-root; then
  echo "WordPress est installé. Activation du plugin Redis..."
  wp plugin activate redis-cache --allow-root || true
  wp redis enable --allow-root || true
else
  echo "WordPress n'est pas encore installé. Redis ne sera pas activé."
fi

# Ramener PHP-FPM au premier plan
echo "Ready. Attente de PHP-FPM..."
exec php-fpm -F
