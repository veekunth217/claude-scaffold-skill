---
name: cicd
description: CI/CD pipeline builder — GitHub Actions, self-hosted runners, Docker build/push, multi-environment deployments, secrets, rollback strategies
version: 1.0.0
author: veekunth217
tags: [cicd, github-actions, self-hosted-runner, docker, pipeline, deployment, rollback, secrets, multi-environment]
platforms: [claude-code, cursor, codex]
---

# CI/CD Skill

Build production-grade CI/CD pipelines — from GitHub Actions workflows to self-hosted runners and zero-downtime deployment strategies.

**RULE: Show complete workflow YAML and explain each job before generating. Wait for GO.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### GitHub Actions Workflows
<!-- TODO: Workflow triggers, reusable workflows, composite actions -->
<!-- TODO: Matrix builds, concurrency groups, path filters -->
<!-- TODO: Caching strategies (npm, pip, docker layers) -->

### Self-Hosted Runner Setup
<!-- TODO: Runner installation on Ubuntu, runner groups -->
<!-- TODO: Docker-based runner, ephemeral runners on EKS -->
<!-- TODO: Security hardening for self-hosted runners -->

### Docker Build & Push Pipeline
<!-- TODO: Multi-platform builds (amd64/arm64), BuildKit cache -->
<!-- TODO: ECR push, GHCR push, tagging strategies (sha, semver, latest) -->
<!-- TODO: Vulnerability scanning in pipeline (Trivy, Snyk) -->

### Multi-Environment Deployments
<!-- TODO: dev → staging → prod promotion flow -->
<!-- TODO: Environment protection rules, required reviewers -->
<!-- TODO: Helm upgrade in pipeline, kubectl apply, ArgoCD sync -->

### Secrets Management in CI
<!-- TODO: GitHub Actions secrets, OIDC to AWS (no long-lived keys) -->
<!-- TODO: Secrets injection into Docker build args vs runtime env -->
<!-- TODO: Rotate secrets without pipeline downtime -->

### Rollback Strategies
<!-- TODO: Helm rollback in pipeline, ArgoCD rollback -->
<!-- TODO: Blue/green switch rollback, database migration rollback -->
<!-- TODO: Automated rollback on health check failure -->

---

## Starter Workflows

### Node.js CI + ECR Push + EKS Deploy
```yaml
name: Deploy
on:
  push:
    branches: [main]

permissions:
  id-token: write   # OIDC
  contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::[account]:role/github-actions-role
          aws-region: [region]

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build & push
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPO:${{ github.sha }} .
          docker push $ECR_REGISTRY/$ECR_REPO:${{ github.sha }}
        env:
          ECR_REGISTRY: [account].dkr.ecr.[region].amazonaws.com
          ECR_REPO: [app-name]

      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --name [cluster] --region [region]
          helm upgrade --install [app] helm/[app] \
            --set image.tag=${{ github.sha }} \
            --values helm/[app]/values-prod.yaml \
            --namespace [ns] --wait
```

### Rollback Job
```yaml
  rollback:
    runs-on: ubuntu-latest
    needs: [build-and-deploy]
    if: failure()
    steps:
      - name: Rollback Helm release
        run: |
          aws eks update-kubeconfig --name [cluster] --region [region]
          helm rollback [app] 0 --namespace [ns]  # 0 = previous revision
```

<!-- TODO: Add full interactive workflow builder for each capability above -->
