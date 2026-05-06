---
name: kubernetes
description: Kubernetes management — Helm charts, ArgoCD GitOps, Ingress, ConfigMaps, HPA autoscaling, blue/green deployments, debugging
version: 1.0.0
author: veekunth217
tags: [kubernetes, k8s, helm, argocd, gitops, ingress, nginx, hpa, blue-green, debugging]
platforms: [claude-code, cursor, codex]
---

# Kubernetes Skill

Production Kubernetes management — from Helm chart authoring to GitOps with ArgoCD and advanced deployment strategies.

**RULE: Always show manifests/plan before applying. Never run `kubectl apply` without showing what changes.**

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

### Helm Chart Creation & Management
<!-- TODO: Chart scaffold, values.yaml design, _helpers.tpl patterns -->
<!-- TODO: Chart testing (helm lint, helm template, helm test) -->
<!-- TODO: Chart versioning, OCI registry push -->

### ArgoCD Setup & GitOps Workflow
<!-- TODO: ArgoCD install on EKS, App-of-Apps pattern -->
<!-- TODO: ApplicationSet, sync policies, automated vs manual -->
<!-- TODO: Image updater, RBAC, SSO integration -->

### Ingress Controllers (nginx)
<!-- TODO: ingress-nginx install, IngressClass, annotations cheatsheet -->
<!-- TODO: TLS termination, rate limiting, rewrite rules, websocket -->

### ConfigMaps & Secrets
<!-- TODO: ConfigMap from file, env injection, volume mounts -->
<!-- TODO: External Secrets Operator (AWS Secrets Manager → k8s Secret) -->
<!-- TODO: Sealed Secrets for GitOps-safe secret storage -->

### HPA Autoscaling
<!-- TODO: CPU/memory HPA, custom metrics (KEDA), VPA -->
<!-- TODO: Cluster autoscaler vs Karpenter -->

### Blue/Green Deployments
<!-- TODO: Manual blue/green with service selectors -->
<!-- TODO: Argo Rollouts blue/green and canary -->
<!-- TODO: Feature flags integration -->

### Kubernetes Debugging
<!-- TODO: Pod crashloop diagnosis flow -->
<!-- TODO: OOMKilled, Pending, ImagePullBackOff, CrashLoopBackOff fixes -->
<!-- TODO: Resource quota issues, node pressure -->
<!-- TODO: Network policy debugging, DNS troubleshooting -->

---

## Common Commands

```bash
# Context management
kubectl config get-contexts
kubectl config use-context [context]

# Debug a failing pod
kubectl describe pod [pod] -n [ns]
kubectl logs [pod] -n [ns] --previous
kubectl exec -it [pod] -n [ns] -- /bin/sh

# Resource pressure
kubectl top nodes
kubectl top pods -n [ns] --sort-by=memory

# Helm
helm list -A                          # all releases
helm history [release] -n [ns]        # rollback history
helm rollback [release] [revision]    # rollback
helm diff upgrade [release] [chart]   # preview changes (requires helm-diff)

# ArgoCD
argocd app list
argocd app sync [app]
argocd app rollback [app] [revision]
```

---

## Helm Chart Stub

```
helm/[app]/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── configmap.yaml
    ├── serviceaccount.yaml
    └── NOTES.txt
```

<!-- TODO: Add full interactive workflows for each capability above -->
