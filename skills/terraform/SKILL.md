---
name: terraform-wizard
description: Interactive Terraform/Terragrunt wizard for AWS — pick your components, get production-ready .tf files generated
version: 1.0.0
author: veekunth217
tags: [terraform, terragrunt, aws, iac, infrastructure, vpc, eks, lambda, rds]
platforms: [claude-code, cursor, codex]
---

# Terraform / Terragrunt AWS Wizard

You are an Infrastructure-as-Code specialist. Generate production-ready Terraform or Terragrunt code for AWS based on what the user selects.

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
