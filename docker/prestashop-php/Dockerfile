FROM php:8.2-fpm

# 1. Dépendances système pour PrestaShop
RUN apt-get update && apt-get install -y \
    unzip wget curl git gnupg \
    netcat-openbsd \
    libzip-dev zip \
    libicu-dev libxml2-dev \
    libpng-dev libjpeg-dev libfreetype6-dev \
    libonig-dev libcurl4-openssl-dev \
    mariadb-client \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install pdo pdo_mysql intl zip gd xml curl mbstring \
 && rm -rf /var/lib/apt/lists/*

# 2. Téléchargement de PrestaShop
ARG PS_VERSION=8.1.4
RUN curl -LO https://github.com/PrestaShop/PrestaShop/releases/download/${PS_VERSION}/prestashop_${PS_VERSION}.zip \
 && unzip prestashop_${PS_VERSION}.zip -d /tmp/ps \
 && mv /tmp/ps/* /var/www/html/ \
 && rm -rf /tmp/ps prestashop_${PS_VERSION}.zip

# 3. Permissions
RUN chown -R www-data:www-data /var/www/html \
 && chmod -R 755 /var/www/html

# 4. Entrypoint custom (BDD wait, settings.inc.php, etc.)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /var/www/html
ENTRYPOINT ["/entrypoint.sh"]
