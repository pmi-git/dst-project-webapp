# Base officielle PHP-FPM avec version stable
FROM php:8.2-fpm

# Mainteneur (optionnel mais pro)
LABEL maintainer="Patrick Miviere <patrick.miviere@gmail.com>"

# Install dependencies & mysqli extension
RUN apt-get update && apt-get install -y \
    unzip \
    wget \
    curl \
    git \
    libpq-dev \
    libzip-dev \
    default-mysql-client \
    && docker-php-ext-install pdo mysqli zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-enable mysqli

# Téléchargement de WordPress (version stable)
ENV WP_VERSION=6.5.3
ENV WP_SHA1=8e4950d39990a2c200a7745d44d32b176baa5ac5

RUN curl -o wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WP_VERSION}.tar.gz" \
    && echo "$WP_SHA1 *wordpress.tar.gz" | sha1sum -c - \
    && tar -xzf wordpress.tar.gz -C /var/www/html --strip-components=1 \
    && rm wordpress.tar.gz

RUN curl -o /usr/local/bin/wp -fSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
  && chmod +x /usr/local/bin/wp \
  && wp --info

# Plugin Redis Object Cache
RUN curl -o redis-cache.zip -fSL https://downloads.wordpress.org/plugin/redis-cache.latest-stable.zip \
    && unzip redis-cache.zip -d /var/www/html/wp-content/plugins \
    && rm redis-cache.zip

# Configuration WordPress (config déjà montée par volume ou git-clonée si besoin)
COPY --chown=www-data:www-data ./wp-config.php /var/www/html/wp-config.php

# Permissions clean
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Santé de PHP-FPM
#HEALTHCHECK --interval=30s --timeout=10s \
#  CMD curl -f http://localhost:9000 || exit 1

# Répertoire de travail
WORKDIR /var/www/html

# Exposer le port FPM
EXPOSE 9000

# Commande par défaut
CMD ["php-fpm"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
