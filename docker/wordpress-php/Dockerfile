# Base officielle PHP-FPM avec version stable
FROM php:8.2-fpm

# Mainteneur (optionnel mais pro)
LABEL maintainer="Patrick Miviere <patrick.miviere@gmail.com>"

# Dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libzip-dev \
    unzip \
    wget \
    gnupg \
    curl \
    git \
    && docker-php-ext-install pdo pdo_pgsql zip

# Téléchargement de WordPress (version stable)
ENV WP_VERSION=6.5.3
ENV WP_SHA1=8e4950d39990a2c200a7745d44d32b176baa5ac5

RUN curl -o wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WP_VERSION}.tar.gz" \
    && echo "$WP_SHA1 *wordpress.tar.gz" | sha1sum -c - \
    && tar -xzf wordpress.tar.gz -C /var/www/html --strip-components=1 \
    && rm wordpress.tar.gz

# Configuration WordPress (config déjà montée par volume ou git-clonée si besoin)
COPY --chown=www-data:www-data ./wp-config.php /var/www/html/wp-config.php

# Permissions clean
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Santé de PHP-FPM
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:9000 || exit 1

# Répertoire de travail
WORKDIR /var/www/html

# Exposer le port FPM
EXPOSE 9000

# Commande par défaut
CMD ["php-fpm"]
