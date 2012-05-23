<?php

define('WP_INSTALLING', true);
define('WP_SITEURL',    '${site_url}');

include 'wp-load.php'; 
include 'wp-admin/includes/upgrade.php';
echo json_encode(wp_install('${blog_title}', '${admin_user}', '${admin_email}', true, '', '${admin_pass}'));
exit();