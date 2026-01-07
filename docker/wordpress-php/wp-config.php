<?php
// Vérification des variables d'environnement critiques
$required_env = ['WORDPRESS_DB_NAME', 'WORDPRESS_DB_USER', 'WORDPRESS_DB_PASSWORD', 'WORDPRESS_DB_HOST'];
foreach ($required_env as $var) {
    if (!getenv($var)) {
        die("❌ Configuration error: missing environment variable '$var'");
    }
}

// Fix pour WP-CLI / contextes sans HTTP_HOST
if (php_sapi_name() === 'cli' || !isset($_SERVER['HTTP_HOST'])) {
  $_SERVER['HTTP_HOST'] = getenv('WP_HOME_HOST') ?: 'localhost:8443';
  $_SERVER['SERVER_NAME'] = $_SERVER['HTTP_HOST'];
  $_SERVER['HTTPS'] = 'on';
}

// Configuration base de données
define( 'DB_NAME', getenv('WORDPRESS_DB_NAME') );
define( 'DB_USER', getenv('WORDPRESS_DB_USER') );
define( 'DB_PASSWORD', getenv('WORDPRESS_DB_PASSWORD') );
define( 'DB_HOST', getenv('WORDPRESS_DB_HOST') );

// Redis config
define('WP_REDIS_HOST', getenv('WP_REDIS_HOST') ?: 'wp-redis');
define('WP_REDIS_PORT', getenv('WP_REDIS_PORT') ?: 6379);
define('WP_REDIS_DISABLED', false);


define('WP_DEBUG', false);
define('WP_DEBUG_DISPLAY', false);
define( 'WP_CACHE', getenv('WP_CACHE') ?: false );

define( 'FS_METHOD', 'direct' );

// Absolut path vers WordPress
if ( ! defined( 'ABSPATH' ) ) {
  define( 'ABSPATH', __DIR__ . '/' );
}

$table_prefix = 'wp_';

// Inclusion du cœur WP
require_once ABSPATH . 'wp-settings.php';