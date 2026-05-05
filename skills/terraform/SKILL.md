---
name: terraform
description: Interactive Terraform/Terragrunt wizard — preset full-stack skeletons (AWS EKS, DigitalOcean Kubernetes) or custom AWS component picker, generates production-ready .tf files
version: 2.0.0
author: veekunth217
tags: [terraform, terragrunt, aws, digitalocean, eks, kubernetes, iac, infrastructure, vpc, rds, doks]
platforms: [claude-code, cursor, codex]
---

# Terraform Wizard — Presets + Component Picker

You are an Infrastructure-as-Code specialist. Generate production-ready Terraform or Terragrunt code based on what the user selects — either a full-stack preset (AWS EKS, DigitalOcean Kubernetes) or a custom AWS component selection.

**RULE: Show the full plan and wait for `GO` before generating any .tf files.**

---

## Step 0 — Pick Your Path

```
What are you building?

  1. AWS EKS full production stack ⭐
     VPC + EKS cluster + IRSA + EBS CSI + ingress-nginx + cert-manager
     Ready-to-apply skeleton modeled on stacksimplify/terraform-on-aws-eks patterns
     ~30 .tf files in modules/{vpc,eks,addons}/

  2. DigitalOcean Kubernetes full stack ⭐
     DOKS cluster + cert-manager + nginx ingress + DNS + sample app namespace
     Modeled on Tythos/accessible-kubernetes-with-terraform-and-digitalocean
     ~20 .tf files in {doproject,certsnamespace,icnamespace,appnamespace}/

  3. Custom AWS components
     Pick exactly what you need: VPC, EKS, RDS, Lambda, S3, Route53, etc.
     (the original component-picker flow — go to Step 1 below)

  4. Empty Terraform skeleton
     Just main.tf + providers.tf + variables.tf + outputs.tf + backend.tf
     For when you want to start from scratch
```

If 1 → jump to **Section A: AWS EKS Preset** below
If 2 → jump to **Section B: DigitalOcean K8s Preset** below
If 3 → continue to Step 1 (the component picker)
If 4 → generate the 5 starter files + a CLAUDE.md and exit

---

## Section A — AWS EKS Full Stack Preset

### A1. Quick questions

```
A few quick questions:

  1. AWS region:           [us-east-1, us-west-2, eu-west-1, ap-south-1, ...]
  2. Project name:         (used as resource prefix — e.g., "myapp")
  3. K8s version:          1.30 (recommended) / 1.29 / 1.28
  4. Node group sizing:    1=small (3× t3.medium), 2=medium (3× t3.large),
                           3=large (5× m6i.xlarge), 4=custom
  5. Domain (optional):    your-app.com (skip for cert-manager + ingress-nginx
                           with default LoadBalancer)
  6. Backend state:        1=S3 + DynamoDB lock (recommended),
                           2=local (dev only — discouraged)
  7. Multi-env (Terragrunt)? y/n — generates dev/staging/prod overlays
```

### A2. Show plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AWS EKS PRESET — PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region:         [region]
Project:        [name]
K8s:            [version]
Node group:     [size]
Domain:         [domain or "none"]
Backend:        [S3+DDB / local]
Multi-env:      [yes/no]

FILE STRUCTURE TO GENERATE:

[project]/
├── main.tf                    # Root module — orchestrates VPC, EKS, addons
├── providers.tf               # aws, kubernetes, helm providers
├── variables.tf               # Root-level inputs
├── outputs.tf                 # cluster_endpoint, kubeconfig, etc.
├── backend.tf                 # S3 + DynamoDB state (or local)
├── terraform.tfvars.example   # Sample values
├── .gitignore                 # *.tfstate, .terraform/
├── CLAUDE.md                  # Project conventions
│
├── modules/
│   ├── vpc/
│   │   ├── main.tf            # VPC + public/private subnets across 3 AZs
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf            # EKS cluster
│   │   ├── nodegroup.tf       # Managed node group
│   │   ├── irsa.tf            # IAM roles for service accounts (OIDC)
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── addons/
│       ├── ebs-csi.tf         # EBS CSI driver via Helm
│       ├── ingress.tf         # ingress-nginx via Helm
│       ├── certmanager.tf     # cert-manager + Let's Encrypt ClusterIssuer
│       ├── metrics-server.tf  # for HPA
│       ├── variables.tf
│       └── outputs.tf
│
└── [if multi-env: terragrunt.hcl + dev/ staging/ prod/ overlays]

KEY DEFAULTS BAKED IN:
  • Private API endpoint with public subnet allow-list
  • OIDC enabled for IRSA
  • EBS gp3 default storage class with encryption
  • cert-manager wired to Let's Encrypt staging (switch to prod after first issue)
  • All resources tagged: Project=[name], ManagedBy=Terraform, Env=[env]

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### A3. Generate files

Generate all the above. Key contents:

**root `main.tf`:**
```hcl
module "vpc" {
  source       = "./modules/vpc"
  project_name = var.project_name
  region       = var.region
  cidr_block   = "10.0.0.0/16"
}

module "eks" {
  source           = "./modules/eks"
  project_name     = var.project_name
  region           = var.region
  k8s_version      = var.k8s_version
  vpc_id           = module.vpc.vpc_id
  private_subnets  = module.vpc.private_subnet_ids
  node_instance_type = var.node_instance_type
  node_count       = var.node_count
}

module "addons" {
  source       = "./modules/addons"
  cluster_name = module.eks.cluster_name
  oidc_arn     = module.eks.oidc_provider_arn
  oidc_url     = module.eks.oidc_provider_url
  domain       = var.domain
}
```

**modules/eks/irsa.tf** (the IRSA pattern from stacksimplify):
```hcl
data "tls_certificate" "eks" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer
}
```

**modules/addons/ingress.tf** (Helm release for ingress-nginx):
```hcl
resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  version          = "4.10.0"
  values = [yamlencode({
    controller = {
      service = {
        annotations = {
          "service.beta.kubernetes.io/aws-load-balancer-type"   = "nlb"
          "service.beta.kubernetes.io/aws-load-balancer-scheme" = "internet-facing"
        }
      }
    }
  })]
}
```

(Generate the full set — the LLM has the patterns, just produce them.)

### A4. Final

```
✓ AWS EKS skeleton generated.

To deploy:
  cd [project]
  cp terraform.tfvars.example terraform.tfvars
  # edit terraform.tfvars with your values
  terraform init
  terraform plan
  terraform apply

After apply:
  aws eks update-kubeconfig --region [region] --name [project]-cluster
  kubectl get nodes
```

---

## Section B — DigitalOcean Kubernetes Preset

### B1. Quick questions

```
A few quick questions:

  1. DO region:        nyc1 / nyc3 / sfo3 / ams3 / sgp1 / lon1 / fra1 / blr1
  2. Project name:     (cluster name + tag)
  3. K8s version:      1.30 / 1.29 / 1.28 (DO uses major.minor only)
  4. Node count:       3 (default — minimum for HA)
  5. Node size:        s-2vcpu-4gb / s-4vcpu-8gb / c-2 / c-4
  6. Domain:           your-app.com — required for cert-manager Let's Encrypt
  7. App namespace:    name for the sample app namespace (default: "www")
```

### B2. Show plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIGITALOCEAN KUBERNETES PRESET — PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region:        [region]
Project:       [name]
K8s:           [version]
Nodes:         [count] × [size]
Domain:        [domain]
App ns:        [name]

FILE STRUCTURE TO GENERATE (Tythos pattern — namespace-based modules):

[project]/
├── main.tf                       # Root — orchestrates 4 namespace modules
├── providers.tf                  # digitalocean + kubernetes + helm
├── variables.tf
├── outputs.tf                    # cluster_id, kubeconfig, lb_ip
├── terraform.tfvars.example
├── .gitignore
├── CLAUDE.md
│
├── doproject/                    # DigitalOcean cluster + project
│   ├── docluster.tf              # digitalocean_kubernetes_cluster
│   ├── doproject.tf              # digitalocean_project for tagging/grouping
│   ├── outputs.tf                # cluster_id, kube_config, host
│   └── providers.tf              # passes provider down
│
├── certsnamespace/               # cert-manager + Let's Encrypt
│   ├── certsnamespace.tf         # k8s namespace
│   ├── certmanagerrelease.tf     # helm_release "cert-manager"
│   ├── clusterissuer.tf          # ClusterIssuer for Let's Encrypt staging+prod
│   ├── dotoksecret.tf            # DO API token secret for DNS-01 challenge
│   ├── outputs.tf
│   └── variables.tf
│
├── icnamespace/                  # ingress controller + DNS records
│   ├── icnamespace.tf            # k8s namespace
│   ├── icrelease.tf              # helm_release "ingress-nginx"
│   ├── dodomain.tf               # digitalocean_domain
│   ├── dorecord.tf               # A record pointing to LB IP
│   ├── data.tf                   # data sources (LB IP from ingress)
│   ├── outputs.tf
│   ├── providers.tf
│   └── variables.tf
│
└── [appns]namespace/             # Your application namespace
    ├── [appns]namespace.tf       # k8s namespace
    ├── [appns]deployment.tf      # sample Deployment (placeholder app)
    ├── [appns]service.tf         # ClusterIP service
    ├── [appns]ingress.tf         # ingress with TLS via cert-manager annotation
    └── variables.tf

KEY DEFAULTS BAKED IN:
  • cert-manager uses DNS-01 challenge via DO API (works for wildcard certs)
  • ingress-nginx pre-wired to cert-manager ClusterIssuer
  • ClusterIP-only service + Ingress (no LoadBalancer per service)
  • All resources tagged with project name in DO Project

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### B3. Generate files

**`doproject/docluster.tf`:**
```hcl
resource "digitalocean_kubernetes_cluster" "main" {
  name    = var.project_name
  region  = var.region
  version = var.k8s_version

  node_pool {
    name       = "default"
    size       = var.node_size
    node_count = var.node_count
    auto_scale = true
    min_nodes  = var.node_count
    max_nodes  = var.node_count * 2
  }

  tags = ["managed-by-terraform", var.project_name]
}
```

**`certsnamespace/clusterissuer.tf`:**
```hcl
resource "kubernetes_manifest" "letsencrypt_prod" {
  manifest = {
    apiVersion = "cert-manager.io/v1"
    kind       = "ClusterIssuer"
    metadata = { name = "letsencrypt-prod" }
    spec = {
      acme = {
        server = "https://acme-v02.api.letsencrypt.org/directory"
        email  = var.acme_email
        privateKeySecretRef = { name = "letsencrypt-prod-key" }
        solvers = [{
          dns01 = {
            digitalocean = {
              tokenSecretRef = {
                name = "digitalocean-dns-token"
                key  = "access-token"
              }
            }
          }
        }]
      }
    }
  }
  depends_on = [helm_release.cert_manager]
}
```

(Generate the full file set following the Tythos pattern.)

### B4. Final

```
✓ DigitalOcean K8s skeleton generated.

To deploy:
  cd [project]
  cp terraform.tfvars.example terraform.tfvars
  # set: do_token, acme_email, project_name, domain
  terraform init
  terraform plan
  terraform apply

After apply (~10 min):
  doctl kubernetes cluster kubeconfig save [project]
  kubectl get pods -A   # cert-manager + ingress-nginx running

Visit:
  https://[domain]/ — your sample app, with auto-issued Let's Encrypt cert
```

---

## Step 1 — Terraform vs Terragrunt

```
Are you using Terraform or Terragrunt?

  1. Terraform — standard .tf files, single workspace or workspaces
  2. Terragrunt — DRY wrapper, multi-environment (dev/staging/prod)
  3. Not sure — recommend one for me

(Terragrunt is recommended for multi-environment setups or teams)
```

If they pick 3: recommend Terragrunt if they mention multiple environments, team, or "prod". Otherwise Terraform.

---

## Step 2 — AWS Region & Project Name

```
Project name (used for resource naming prefix): ___
AWS region (e.g. us-east-1, ap-south-1): ___
```

---

## Step 3 — Component Checklist

Show this checklist. User types numbers to select (or "all"):

```
Select the AWS components you need:
(type numbers separated by spaces, or "all")

NETWORKING
  [1]  VPC + Subnets (public/private)
  [2]  Internet Gateway
  [3]  NAT Gateway
  [4]  Security Groups
  [5]  VPC Endpoints

COMPUTE
  [6]  EC2 Instances + Auto Scaling Group
  [7]  EKS Cluster (managed Kubernetes)
  [8]  ECS + Fargate
  [9]  Lambda Functions
  [10] Elastic Load Balancer (ALB/NLB)

CONTAINERS
  [11] ECR (Elastic Container Registry)

STORAGE
  [12] S3 Buckets
  [13] EBS Volumes
  [14] EFS (shared filesystem)

DATABASE
  [15] RDS (PostgreSQL / MySQL)
  [16] DynamoDB
  [17] ElastiCache (Redis)

CDN & DNS
  [18] CloudFront Distribution
  [19] Route 53 Hosted Zone + Records
  [20] ACM SSL Certificate

SECURITY & IAM
  [21] IAM Roles + Policies
  [22] KMS Keys
  [23] Secrets Manager
  [24] WAF

MONITORING
  [25] CloudWatch Alarms + Dashboards
  [26] CloudWatch Log Groups

> 
```

---

## Step 4 — Environment Setup (Terragrunt only)

If Terragrunt was selected:
```
Which environments do you need?
  1. dev + prod
  2. dev + staging + prod
  3. Custom (list them)
```

---

## Step 5 — Show Structure and Confirm

**For Terraform:**
```
I'll generate this structure:
  [project-name]/
  ├── main.tf
  ├── variables.tf
  ├── outputs.tf
  ├── providers.tf
  ├── terraform.tfvars.example
  └── modules/
      ├── vpc/          (if selected)
      ├── eks/          (if selected)
      ├── rds/          (if selected)
      └── ...

Type GO to generate all files.
```

**For Terragrunt:**
```
  [project-name]/
  ├── terragrunt.hcl          (root config)
  ├── _modules/
  │   ├── vpc/
  │   ├── eks/
  │   └── ...
  ├── dev/
  │   ├── terragrunt.hcl
  │   ├── vpc/terragrunt.hcl
  │   └── ...
  └── prod/
      ├── terragrunt.hcl
      └── ...
```

---

## Step 6 — Generate Files

Generate complete, working file content for each selected component. Use these patterns:

### providers.tf (always)
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # Uncomment to use S3 backend
  # backend "s3" {
  #   bucket = "[project-name]-terraform-state"
  #   key    = "terraform.tfstate"
  #   region = "[region]"
  # }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

### VPC Module (component 1-5)
Generate a complete `modules/vpc/main.tf` with:
- VPC resource with CIDR `10.0.0.0/16`
- Public subnets across 2 AZs (`10.0.1.0/24`, `10.0.2.0/24`)
- Private subnets across 2 AZs (`10.0.10.0/24`, `10.0.11.0/24`)
- Internet Gateway (if selected)
- NAT Gateway in public subnet (if selected) — one per AZ for prod, one for dev
- Route tables for public and private subnets

### EKS Module (component 7)
Generate `modules/eks/main.tf` with:
- `aws_eks_cluster` using private subnets
- `aws_eks_node_group` with managed nodes
- IAM roles: cluster role + node group role with required policies
- Security group for cluster API
- `aws_eks_addon` for coredns, kube-proxy, vpc-cni

After EKS is selected, also ask:
```
Do you want Helm chart deployments on EKS?
  1. Yes — generate Helm provider + chart releases in Terraform
  2. Yes — generate a starter Helm chart for my app
  3. Both
  4. No
```

**Helm provider in Terraform (option 1):**
```hcl
# modules/eks/helm.tf
provider "helm" {
  kubernetes {
    host                   = aws_eks_cluster.[name].endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.[name].certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.[name].name]
      command     = "aws"
    }
  }
}

# Example: deploy ingress-nginx via Terraform + Helm
resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true
  version          = "4.10.0"

  set { name = "controller.service.type"; value = "LoadBalancer" }
  set { name = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/aws-load-balancer-type"; value = "nlb" }
}

# Example: AWS Load Balancer Controller
resource "helm_release" "aws_lbc" {
  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"

  set { name = "clusterName";     value = aws_eks_cluster.[name].name }
  set { name = "serviceAccount.create"; value = "false" }
  set { name = "serviceAccount.name";   value = "aws-load-balancer-controller" }
}
```

**Starter Helm chart for the user's app (option 2/3):**
Generate `helm/[app-name]/` with:
```
helm/[app-name]/
├── Chart.yaml
├── values.yaml               # dev defaults
├── values-prod.yaml          # prod overrides
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml               # Horizontal Pod Autoscaler
    ├── configmap.yaml
    ├── secret.yaml
    └── _helpers.tpl
```

Key `values.yaml`:
```yaml
replicaCount: 2
image:
  repository: [aws-account-id].dkr.ecr.[region].amazonaws.com/[app-name]
  tag: latest
  pullPolicy: Always
service:
  type: ClusterIP
  port: 80
  targetPort: 3000
ingress:
  enabled: true
  className: nginx
  host: [domain]
  tls: true
resources:
  requests: { cpu: 100m, memory: 128Mi }
  limits:   { cpu: 500m, memory: 512Mi }
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### ECR (component 11)
```hcl
resource "aws_ecr_repository" "[project_name]" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
resource "aws_ecr_lifecycle_policy" "[project_name]" {
  repository = aws_ecr_repository.[project_name].name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = { tagStatus = "any", countType = "imageCountMoreThan", countNumber = 10 }
      action = { type = "expire" }
    }]
  })
}
```

### Lambda (component 9)
Generate `modules/lambda/main.tf` with:
- `aws_lambda_function` with placeholder zip
- IAM role with basic execution + CloudWatch logs
- `aws_cloudwatch_log_group` with 30-day retention
- Optional: `aws_lambda_function_url` for direct invocation

### RDS (component 15)
Generate `modules/rds/main.tf` with:
- `aws_db_instance` (PostgreSQL 15 default, configurable)
- `aws_db_subnet_group` using private subnets
- Security group allowing access from VPC CIDR only
- `random_password` for master password stored in Secrets Manager

### Terragrunt Root Config
```hcl
# terragrunt.hcl (root)
locals {
  project_name = "[project-name]"
  aws_region   = "[region]"
}

generate "provider" {
  path      = "providers.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
}
EOF
}

remote_state {
  backend = "s3"
  generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
  config = {
    bucket  = "${local.project_name}-tfstate-${get_aws_account_id()}"
    key     = "${path_relative_to_include()}/terraform.tfstate"
    region  = local.aws_region
    encrypt = true
    dynamodb_table = "${local.project_name}-tfstate-lock"
  }
}
```

---

## Step 7 — Next Steps

After generating all files:

```
✓ Infrastructure code generated.

To deploy:
  cd [project-name]
  terraform init
  terraform plan -var-file="terraform.tfvars"
  terraform apply -var-file="terraform.tfvars"

For Terragrunt:
  cd [project-name]/dev
  terragrunt run-all init
  terragrunt run-all plan
  terragrunt run-all apply

Recommended next skills:
  • GSD (gsd-build/get-shit-done) — plan your infra work in phases
  • Claude Code Toolkit — structured task execution

Useful tools:
  • infracost (cost estimation): https://www.infracost.io
  • tfsec (security scan): brew install tfsec && tfsec .
  • terraform-docs: brew install terraform-docs
```
