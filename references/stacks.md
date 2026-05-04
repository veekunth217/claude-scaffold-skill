# Supported Stacks Reference

This file is loaded on-demand by the scaffolding wizard. It is not loaded into context automatically.

---

## Frontend Stacks

### React (Vite + TypeScript)
- **Node.js required:** >= 18.0.0
- **Recommended Node version manager:** nvm
- **Scaffold command:** `npx create-vite@latest my-app -- --template react-ts`
- **Dev server:** `npm run dev`
- **Build:** `npm run build`
- **Default port:** 5173

### Vue 3 (Vite + TypeScript)
- **Node.js required:** >= 18.0.0
- **Scaffold command:** `npx create-vite@latest my-app -- --template vue-ts`
- **Dev server:** `npm run dev`
- **Default port:** 5173

### Angular
- **Node.js required:** >= 18.13.0
- **Scaffold command:** `npx @angular/cli@latest new my-app --strict`
- **Dev server:** `ng serve` or `npx ng serve`
- **Default port:** 4200

### Next.js
- **Node.js required:** >= 18.17.0
- **Scaffold command:** `npx create-next-app@latest my-app --typescript --tailwind --eslint --app`
- **Dev server:** `npm run dev`
- **Default port:** 3000

### Hugo
- **Hugo binary required:** >= 0.110.0
- **Install (Mac):** `brew install hugo`
- **Install (Linux):** `sudo snap install hugo` or download from github.com/gohugoio/hugo/releases
- **Install (Windows):** `choco install hugo-extended`
- **Scaffold command:** `hugo new site my-site`
- **Dev server:** `hugo server -D`
- **Default port:** 1313

---

## Backend Stacks

### Node.js / Express
- **Node.js required:** >= 18.0.0
- **Key packages:** `express`, `dotenv`, `cors`
- **Dev packages:** `nodemon`, `typescript`, `ts-node`, `@types/node`, `@types/express`
- **Dev server:** `npx nodemon src/index.ts`
- **Default port:** 3000

### Python / FastAPI
- **Python required:** >= 3.10
- **Recommended version manager:** pyenv
- **Key packages:** `fastapi`, `uvicorn[standard]`, `python-dotenv`
- **Dev packages:** `pytest`, `httpx`, `ruff`
- **Dev server:** `uvicorn main:app --reload`
- **Default port:** 8000
- **Virtual env:** Always create `.venv` — never install globally

### PHP / Laravel
- **PHP required:** >= 8.2
- **Composer required:** latest stable
- **Scaffold command:** `composer create-project laravel/laravel my-app`
- **Dev server:** `php artisan serve`
- **Default port:** 8000

---

## CMS

### WordPress
- **PHP required:** >= 8.1
- **MySQL required:** >= 8.0 (or MariaDB >= 10.4)
- **Web server:** Apache (with mod_rewrite) or Nginx
- **Download:** `curl -O https://wordpress.org/latest.tar.gz`
- **WooCommerce:** Install via WP admin Plugins > Add New after WordPress setup

**Database setup (MySQL):**
```sql
CREATE DATABASE wordpress_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wp_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Full-Stack Stacks

### MERN (MongoDB + Express + React + Node)
- **Node.js required:** >= 18.0.0
- **MongoDB:** local install or MongoDB Atlas (recommended for VPS)
- **Structure:**
  ```
  my-app/
  ├── server/     # Express + Mongoose API
  ├── client/     # React (Vite + TS)
  └── docker-compose.yml  (optional)
  ```

### LAMP (Linux + Apache + MySQL + PHP)
- **Install (apt):**
  ```bash
  sudo apt update
  sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql
  sudo systemctl enable apache2 mysql
  ```
- **Web root:** `/var/www/html/`
- **Config:** `/etc/apache2/sites-available/`

### LEMP (Linux + Nginx + MySQL + PHP)
- **Install (apt):**
  ```bash
  sudo apt update
  sudo apt install nginx mysql-server php-fpm php-mysql
  sudo systemctl enable nginx mysql php8.2-fpm
  ```
- **Web root:** `/var/www/html/`
- **Config:** `/etc/nginx/sites-available/`
- **PHP-FPM socket:** `/var/run/php/php8.2-fpm.sock`

---

## Infrastructure

### Terraform
- **Terraform required:** >= 1.5.0
- **Install (Mac):** `brew install terraform` or via tfenv
- **Install (Linux):** Download from releases.hashicorp.com or use tfenv
- **Recommended:** tfenv (version manager for Terraform)
- **Init:** `terraform init`
- **Plan:** `terraform plan`
- **Apply:** `terraform apply`
- **Suggested structure:**
  ```
  my-infra/
  ├── main.tf
  ├── variables.tf
  ├── outputs.tf
  ├── providers.tf
  └── modules/
  ```

### Docker Compose
- **Docker required:** >= 24.0
- **Docker Compose plugin required:** >= 2.0 (comes bundled with Docker Desktop)
- **Install (Linux):** `curl -fsSL https://get.docker.com | sh`
- **Verify:** `docker compose version`
- **Start:** `docker compose up -d`
- **Stop:** `docker compose down`

---

## Version Manager Reference

| Language | Manager | Install (Mac) | Install (Linux) |
|----------|---------|---------------|-----------------|
| Node.js  | nvm     | `brew install nvm` | `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh \| bash` |
| Python   | pyenv   | `brew install pyenv` | `curl https://pyenv.run \| bash` |
| Ruby     | rbenv   | `brew install rbenv` | `curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer \| bash` |
| Terraform| tfenv   | `brew install tfenv` | github.com/tfutils/tfenv |
