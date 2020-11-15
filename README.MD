# Provision light blog in 10 minutes

1. Fork this repository, clone it and make sure to check out branch `light-blogs-with-dynamodb`
2. `cd deployment\nosql`, and run the following commands to provision DynamoDB Service

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

3. `cd deployment\load-balancer`, and run the following commands to provision Load Balance and Auto Scale Service

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

After successfully provisioning, you will get output like below:

```bash
Apply complete! Resources: 10 added, 0 changed, 0 destroyed.

Outputs:

alb_dns_name = alb-1-843275519.ap-northeast-1.elb.amazonaws.com
```

you can enter your *alb_dns_name* in browser to check the result.

The environment you just provision is composed of several parts as shown below:

![](https://2cloudlab.com/images/blog/load-balance-nosql-cloud-computing-WSGI-python-gunicorn-supervisior-nginx-ec2.png)

**NOTE**: The environment will incur cost, so if you don't need it any more, run the following steps to destroy it

1. `cd deployment\load-balancer` and run `terraform destroy -auto-approve`
2. `cd deployment\nosql` and run `terraform destroy -auto-approve`

If destroy successfully, you will get similar output shown below:

```bash
Destroy complete! Resources: 10 destroyed.
```

You can provide your own web-app instead of the light blog, and depend on the same environment provisioned above, checkout [here](https://github.com/digolds/digolds_sample) to find out how to accomplish it.