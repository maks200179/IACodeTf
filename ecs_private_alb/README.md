# ECS Fargate behind Public ALB (Private Subnets) — HTTPS Ready

This Terraform package deploys:
- VPC with **2 public** and **2 private** subnets
- **Internet Gateway** for public subnets and **NAT Gateway** for private egress
- Public **Application Load Balancer** (ALB) in public subnets
- **ECS Fargate** cluster & service (tasks in **private** subnets, no public IPs)
- **HTTP → HTTPS** redirect on port 80
- Optional **HTTPS (443)** listener using an **existing ACM certificate ARN** (manual validation)

## Quick Start

```bash
terraform init
terraform apply -auto-approve
```

After apply, Terraform will print the `alb_dns_name`. Visit it in your browser.

## Enabling HTTPS (Manual ACM Validation)

1. In the AWS Console (same region as your ALB), request a public ACM certificate for your domain (e.g., `app.example.com`). Choose **DNS validation**.
2. Create the DNS validation CNAME record(s) in your DNS provider.
3. Wait until the certificate status becomes **Issued**.
4. Copy the **Certificate ARN**.
5. Set variables to enable HTTPS:

Create a `terraform.tfvars` (or pass via `-var`) with:
```hcl
enable_https       = true
acm_certificate_arn = "arn:aws:acm:REGION:ACCOUNT:certificate/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Then apply again:
```bash
terraform apply
```

Now the ALB serves HTTPS on port 443 and HTTP will redirect to HTTPS.

## Customization

- Change region: edit `variables.tf` (default `us-east-1`) or set `-var="region=ca-central-1"`.
- Change image: set `-var="container_image=yourrepo/yourapp:tag"`.
- Scale tasks: set `-var="service_desired_count=2"`.
- Change container port: `-var="container_port=8080"` (remember to adjust health checks on your app).

## Clean Up

```bash
terraform destroy
```

> Note: NAT Gateway incurs charges while running. Destroy when done.

## Files

- `versions.tf` — Terraform & provider constraints
- `provider.tf` — AWS provider
- `variables.tf` — Adjustable inputs
- `main.tf` — Full networking, ALB, ECS, and listeners
- `outputs.tf` — Useful outputs
- `README.md` — This guide
```