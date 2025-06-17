<?php
define( 'DB_NAME', getenv('WORDPRESS_DB_NAME') ?: 'wordpress' );
define( 'DB_USER', getenv('WORDPRESS_DB_USER') ?: 'wpuser' );
define( 'DB_PASSWORD', getenv('WORDPRESS_DB_PASSWORD') ?: 'wppass' );
define( 'DB_HOST', getenv('WORDPRESS_DB_HOST') ?: 'mysql' );

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