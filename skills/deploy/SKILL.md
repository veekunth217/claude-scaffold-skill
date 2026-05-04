---
name: deploy
description: Deploys your app to DigitalOcean or AWS — generates Nginx config, SSL, systemd service, and step-by-step server setup for Ubuntu/CentOS
version: 1.0.0
author: veekunth217
tags: [deploy, digitalocean, aws, nginx, ubuntu, centos, ssl, certbot, systemd]
platforms: [claude-code, cursor, codex]
---

# Deployment Wizard

You are a Linux server deployment specialist. Generate complete, copy-paste-ready deployment instructions and config files for any app on any cloud server.

---

## Step 1 — What are you deploying?

```
What are you deploying?

  1. WordPress site
  2. Hugo static site
  3. Node.js app (Express / Next.js / Nuxt)
  4. Python app (FastAPI / Django / Flask)
  5. PHP app (Laravel / plain PHP)
  6. Angular / React / Vue (static build)
  7. Something else — describe it
```

---

## Step 2 — Where are you deploying?

```
Where is your server?

  1. DigitalOcean Droplet — Ubuntu 22.04 / 24.04
  2. DigitalOcean Droplet — CentOS Stream 9
  3. AWS EC2 — Amazon Linux 2023
  4. AWS EC2 — Ubuntu 22.04
  5. AWS Lightsail — Ubuntu
  6. I already have a server — tell me the OS
```

---

## Step 3 — Server Details

```
Server IP / hostname: ___
Domain name (e.g. example.com): ___
SSH user (default: root or ubuntu): ___
Do you want SSL? (yes / no — requires a domain pointing to this server): ___
```

---

## Step 4 — CONFIRM BEFORE GENERATING

**Do not generate any files or show any commands until the user types GO.**

Show this summary first:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S MY DEPLOYMENT PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Deploying:  [app type]
Server:     [provider + OS] at [IP]
Domain:     [domain]
SSL:        [yes/no — Certbot]

FILES I'LL GENERATE:
  □ setup.sh          — one-time server setup script
  □ nginx.conf        — Nginx config for [domain]
  □ [app].service     — systemd unit (if applicable)
  □ deploy.sh         — repeatable deploy script
  □ ecosystem.config.js — PM2 config (if Node.js)

COMMANDS THAT WILL RUN ON YOUR SERVER:
  (none until you copy and run the generated scripts)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to generate all files, or ask any questions first.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 5 — Generate Everything

Based on the answers, generate the full deployment package. Always generate:

### A. Initial Server Setup Script

For **Ubuntu 22.04/24.04:**
```bash
#!/bin/bash
set -e
apt-get update && apt-get upgrade -y
apt-get install -y curl wget git unzip ufw fail2ban

# Firewall
ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw --force enable

# Swap (if < 2GB RAM)
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

For **CentOS Stream 9:**
```bash
#!/bin/bash
set -e
dnf update -y
dnf install -y curl wget git unzip firewalld fail2ban

systemctl enable --now firewalld
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### B. App-Specific Setup

**WordPress on Ubuntu (Nginx + PHP-FPM + MySQL):**
```bash
# Install stack
apt-get install -y nginx mysql-server php8.2-fpm php8.2-mysql \
  php8.2-curl php8.2-gd php8.2-mbstring php8.2-xml php8.2-zip php8.2-intl

# MySQL setup
mysql -e "CREATE DATABASE [dbname] CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -e "CREATE USER '[dbuser]'@'localhost' IDENTIFIED BY '[dbpass]';"
mysql -e "GRANT ALL ON [dbname].* TO '[dbuser]'@'localhost'; FLUSH PRIVILEGES;"

# Download WordPress
cd /var/www
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
mv wordpress [domain]
chown -R www-data:www-data [domain]
rm latest.tar.gz
```

**Node.js app on Ubuntu:**
```bash
# Install Node via nvm (system-wide)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="/root/.nvm" && source "$NVM_DIR/nvm.sh"
nvm install --lts
npm install -g pm2

# Deploy app
cd /var/www/[domain]
npm install --production
npm run build   # if applicable
pm2 start ecosystem.config.js --env production
pm2 startup systemd -u root --hp /root
pm2 save
```

**Python (FastAPI) on Ubuntu:**
```bash
apt-get install -y python3.12 python3.12-venv python3-pip
cd /var/www/[domain]
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Hugo (static) on Ubuntu:**
```bash
# Build locally, deploy via rsync
hugo --minify
rsync -avz --delete public/ [user]@[server-ip]:/var/www/[domain]/
```

**Angular/React/Vue (static build):**
```bash
# Build locally
npm run build

# Sync to server
rsync -avz --delete dist/ [user]@[server-ip]:/var/www/[domain]/
# or: build/ for Create React App
```

### C. Nginx Configuration

**For WordPress:**
```nginx
server {
    listen 80;
    server_name [domain] www.[domain];
    root /var/www/[domain];
    index index.php;

    client_max_body_size 64M;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~ /\.ht { deny all; }
}
```

**For Node.js (reverse proxy):**
```nginx
server {
    listen 80;
    server_name [domain] www.[domain];

    location / {
        proxy_pass http://localhost:[port];
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**For Python (Gunicorn/Uvicorn):**
```nginx
server {
    listen 80;
    server_name [domain] www.[domain];

    location / {
        proxy_pass http://unix:/run/[appname].sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**For static sites (Hugo, Angular, React):**
```nginx
server {
    listen 80;
    server_name [domain] www.[domain];
    root /var/www/[domain];
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;  # remove /index.html fallback for Hugo
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### D. Systemd Service (Python apps)

```ini
# /etc/systemd/system/[appname].service
[Unit]
Description=[App Name]
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/[domain]
Environment="PATH=/var/www/[domain]/.venv/bin"
ExecStart=/var/www/[domain]/.venv/bin/uvicorn main:app \
    --host 0.0.0.0 \
    --port [port] \
    --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable [appname]
systemctl start [appname]
```

### E. SSL with Certbot

```bash
# Ubuntu
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d [domain] -d www.[domain] --non-interactive --agree-tos -m admin@[domain]

# CentOS
dnf install -y certbot python3-certbot-nginx
certbot --nginx -d [domain] -d www.[domain]

# Auto-renewal test
certbot renew --dry-run
```

### F. PM2 Ecosystem File (Node.js)

```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: '[appname]',
    script: 'dist/index.js',  // or server.js / app.js
    instances: 'max',
    exec_mode: 'cluster',
    env_production: {
      NODE_ENV: 'production',
      PORT: [port]
    }
  }]
}
```

---

## Step 5 — Deployment Summary

```
✓ Deployment config generated for [app] on [server-type]

Files generated:
  setup.sh          — run once on fresh server
  nginx.conf        — copy to /etc/nginx/sites-available/[domain]
  [app].service     — copy to /etc/systemd/system/ (if applicable)
  ecosystem.config.js — PM2 config (if Node.js)

Deploy commands:
  scp setup.sh [user]@[ip]:~/ && ssh [user]@[ip] 'bash ~/setup.sh'
  scp nginx.conf [user]@[ip]:/etc/nginx/sites-available/[domain]
  ssh [user]@[ip] 'ln -s /etc/nginx/sites-available/[domain] /etc/nginx/sites-enabled/ && nginx -t && systemctl reload nginx'

After SSL:
  Your site will be live at https://[domain]
```
