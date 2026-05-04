---
name: wordpress
description: WordPress site, plugin, or theme wizard — scaffolds locally, sets up dev environment, and deploys to DigitalOcean or any Ubuntu server
version: 1.0.0
author: veekunth217
tags: [wordpress, wp, plugin, theme, woocommerce, php, mysql, deploy]
platforms: [claude-code, cursor, codex]
---

# WordPress Wizard

You are a WordPress specialist. Help the user build and deploy WordPress projects — sites, plugins, or themes — with proper tooling and skill recommendations.

---

## Step 1 — What type of WordPress project?

```
What are you building?

  1. WordPress site (new installation + theme)
  2. WordPress plugin (custom functionality)
  3. WordPress theme (custom design)
  4. WooCommerce store (shop + payment)
  5. WooCommerce plugin/addon

```

---

## Step 2 — Branch by Type

### Branch A: WordPress Site / WooCommerce Store

Ask:
```
  Hosting target:
    1. I'll deploy to DigitalOcean Ubuntu — set it up for me
    2. I already have a server — give me install steps
    3. Local dev only (DDEV / LocalWP / Docker)

  Domain name: ___
  Admin email: ___
  Install WooCommerce? (yes/no)
  Install a page builder? (Elementor / Bricks / none)
```

For local dev with DDEV:
```bash
# Install DDEV (Mac)
brew install ddev/ddev/ddev

# Create project
mkdir [site-name] && cd [site-name]
ddev config --project-type=wordpress --php-version=8.2
ddev start
ddev wp core download
ddev wp config create --dbname=db --dbuser=db --dbpass=db --dbhost=db
ddev wp core install \
  --url=$(ddev describe -j | jq -r '.raw.primary_url') \
  --title="[Site Name]" \
  --admin_user=admin \
  --admin_password=admin \
  --admin_email=[email]

# WooCommerce
ddev wp plugin install woocommerce --activate
```

For server deployment → invoke `skills/deploy/SKILL.md` WordPress flow.

---

### Branch B: WordPress Plugin

Ask:
```
  Plugin name: ___
  Plugin slug (lowercase-hyphenated): ___
  Plugin type:
    1. General utility plugin
    2. Shortcode plugin
    3. Gutenberg block plugin
    4. WooCommerce addon
    5. REST API plugin
  Namespace/vendor prefix (e.g. MyPlugin, Acme): ___
```

Generate the full plugin boilerplate:

**File structure:**
```
[plugin-slug]/
├── [plugin-slug].php          # Main plugin file
├── includes/
│   ├── class-[plugin-slug].php
│   ├── class-[plugin-slug]-loader.php
│   └── class-[plugin-slug]-activator.php
├── admin/
│   ├── class-[plugin-slug]-admin.php
│   └── css/ js/ partials/
├── public/
│   ├── class-[plugin-slug]-public.php
│   └── css/ js/
├── languages/
│   └── [plugin-slug].pot
├── tests/
│   ├── test-[plugin-slug].php
│   └── bootstrap.php
├── composer.json
├── phpunit.xml
└── README.txt
```

**Main plugin file:**
```php
<?php
/**
 * Plugin Name:       [Plugin Name]
 * Plugin URI:        https://example.com/[plugin-slug]
 * Description:       [Description]
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      8.1
 * Author:            [Author]
 * License:           GPL v2 or later
 * Text Domain:       [plugin-slug]
 */

if ( ! defined( 'ABSPATH' ) ) exit;

define( '[PLUGIN_CONST]_VERSION', '1.0.0' );
define( '[PLUGIN_CONST]_DIR', plugin_dir_path( __FILE__ ) );
define( '[PLUGIN_CONST]_URL', plugin_dir_url( __FILE__ ) );

require_once [PLUGIN_CONST]_DIR . 'includes/class-[plugin-slug].php';

function run_[plugin_underscore](): void {
    $plugin = new [PluginClass]();
    $plugin->run();
}
run_[plugin_underscore]();
```

**For Gutenberg block plugin**, also generate:
```bash
# Use @wordpress/create-block
npx @wordpress/create-block@latest [plugin-slug] --namespace [namespace]
```

**For WooCommerce addon**, add:
```php
// Check WooCommerce is active
if ( ! in_array( 'woocommerce/woocommerce.php', apply_filters( 'active_plugins', get_option( 'active_plugins' ) ) ) ) {
    add_action( 'admin_notices', function() {
        echo '<div class="error"><p>This plugin requires WooCommerce.</p></div>';
    });
    return;
}
```

---

### Branch C: WordPress Theme

Ask:
```
  Theme name: ___
  Theme type:
    1. Classic theme (PHP templates)
    2. Block theme (Full Site Editing, theme.json)
    3. Child theme of: ___
  Use a starter? (underscores.me / no)
```

For `_s` (underscores) starter:
```bash
curl -o [theme-slug].zip "https://underscores.me/?_s=[theme-slug]&sassify=1"
unzip [theme-slug].zip -d wp-content/themes/
```

For block theme, generate `theme.json` with color palette, typography, and layout settings.

---

## Step 3 — Development Tools

Always suggest:
```bash
# WP-CLI (essential for WP development)
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp

# Composer (for plugin dependencies)
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer

# PHPUnit for plugin testing
composer require --dev phpunit/phpunit wp-phpunit/wp-phpunit
```

---

## Step 4 — Recommended Skills

After scaffolding, recommend these skills for the bootstrapper:

**Always for WordPress:**
- GSD (`gsd-build/get-shit-done`) — plan plugin features in phases
- Claude Code Expert — workflow and code review

**For plugin development:**
- Browser Use / Chromium Testing — automated testing of plugin UI in WordPress admin
- Code Review Graph — trace plugin hook dependencies
- UI/UX Pro Max — if building admin UI or Gutenberg blocks

**For WooCommerce:**
- All of the above + Agent Orchestrator for complex multi-step store setups

Tell the user:
```
Skill recommendation for your WordPress project:

  Essential:  GSD + Claude Code Expert
  For testing: Add a Chromium/browser-use skill to automate
               WP admin and front-end testing
  For UI:     UI/UX Pro Max helps design Gutenberg blocks
              and admin pages that match WP design language

Run /skill-bootstrap to install these now.
```

---

## Step 4 — CONFIRM BEFORE GENERATING

**Do not generate any code or run any commands until the user types GO.**

Show this before anything is created:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S MY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Building:   WordPress [site/plugin/theme] — [name]
Mode:       [Fresh install / Plugin boilerplate / Theme]
Local dev:  [DDEV / Docker / None]
Deploy to:  [Server details or "not yet"]

FILES I'LL CREATE:
  [full list based on type]

COMMANDS I'LL RUN:
  [list — e.g. ddev config, ddev start, wp core download]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to proceed, or ask anything first.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 5 — Deployment

If deployment was requested → invoke `skills/deploy/SKILL.md` with:
- App type: WordPress
- Target: what the user specified

Otherwise:
```
To deploy this WordPress site later, run: /deploy
It will set up Nginx + PHP-FPM + MySQL + SSL on your server.
```
