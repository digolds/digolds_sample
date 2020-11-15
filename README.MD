# Provision Web App in 1 hour

1. Develop your own Web App, and put all executable files in folder *personal-blog*
2. `cd deployment\nosql`, and run the following commands to provision DynamoDB Service

```bash
terraform init
terraform plan
terraform apply
```

3. `cd deployment\load-balancer`, and run the following commands to provision Load Balance and Auto Scale Service

```bash
terraform init
terraform plan
terraform apply
```