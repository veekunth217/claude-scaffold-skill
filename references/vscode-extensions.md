# VS Code Extension Recommendations by Stack

Used by `/scaffold` post-step to populate `.vscode/extensions.json`.

The base set (always include):

```
anthropic.claude-code        ← primary AI assistant
rooveterinaryinc.roo-cline   ← secondary AI for handoffs
eamodio.gitlens              ← inline git blame, history
editorconfig.editorconfig    ← consistent indent/eol
streetsidesoftware.code-spell-checker
```

## Stack-specific additions

### Node.js / TypeScript

```
dbaeumer.vscode-eslint
esbenp.prettier-vscode
ms-vscode.vscode-typescript-next
mikestead.dotenv
prisma.prisma             (if Prisma)
bradlc.vscode-tailwindcss (if Tailwind)
```

### React / Next.js

(everything above plus)

```
formulahendry.auto-rename-tag
burkeholland.simple-react-snippets
ms-vscode.vscode-js-debug
```

### Python

```
ms-python.python
ms-python.vscode-pylance
charliermarsh.ruff
ms-python.black-formatter
```

### PHP / WordPress

```
bmewburn.vscode-intelephense-client
xdebug.php-debug
johnbillion.vscode-wordpress-hooks  (if WP)
```

### Terraform

```
hashicorp.terraform
hashicorp.hcl
4ops.terraform                      (alternative — pick one)
```

### Docker / Kubernetes

```
ms-azuretools.vscode-docker
ms-kubernetes-tools.vscode-kubernetes-tools
redhat.vscode-yaml
tim-koehler.helm-intellisense       (if Helm)
```

### Rust

```
rust-lang.rust-analyzer
serayuzgur.crates
tamasfe.even-better-toml
```

### Go

```
golang.go
```

## Stack-specific settings.json overrides

### Python

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": { "source.organizeImports": "explicit" }
  },
  "python.analysis.typeCheckingMode": "strict",
  "python.testing.pytestEnabled": true
}
```

### Node / TypeScript

```json
{
  "[javascript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescript]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[typescriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### Terraform

```json
{
  "[terraform]": { "editor.defaultFormatter": "hashicorp.terraform" },
  "[terraform-vars]": { "editor.defaultFormatter": "hashicorp.terraform" },
  "terraform.experimentalFeatures.validateOnSave": true
}
```

### PHP

```json
{
  "[php]": { "editor.defaultFormatter": "bmewburn.vscode-intelephense-client" },
  "intelephense.environment.phpVersion": "8.3.0"
}
```

## Stack-specific tasks.json commands

| Stack | dev | test | build | lint |
|---|---|---|---|---|
| Node + Vite | `npm run dev` | `npm test` | `npm run build` | `npm run lint` |
| Next.js | `npm run dev` | `npm test` | `npm run build` | `npm run lint` |
| FastAPI | `uvicorn src.app.main:app --reload` | `pytest` | `python -m build` | `ruff check .` |
| Django | `python manage.py runserver` | `python manage.py test` | `python manage.py collectstatic --noinput` | `ruff check .` |
| WordPress plugin | `wp-env start` | `composer test` | `composer build` | `composer phpcs` |
| Terraform | `terraform plan` | `terraform validate` | `terraform apply -auto-approve` | `terraform fmt -recursive` |
| Go | `go run .` | `go test ./...` | `go build` | `golangci-lint run` |
| Rust | `cargo run` | `cargo test` | `cargo build --release` | `cargo clippy` |
