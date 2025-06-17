<?php
define( 'DB_NAME', getenv('WORDPRESS_DB_NAME') ?: 'wordpress' );
define( 'DB_USER', getenv('WORDPRESS_DB_USER') ?: 'wpuser' );
define( 'DB_PASSWORD', getenv('WORDPRESS_DB_PASSWORD') ?: 'wppass' );
define( 'DB_HOST', getenv('WORDPRESS_DB_HOST') ?: 'postgres' );

define( 'WP_DEBUG', getenv('WP_DEBUG') ?: false );
define( 'WP_CACHE', getenv('WP_CACHE') ?: false );

define( 'FS_METHOD', 'direct' );
