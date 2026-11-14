# infra/backend.hcl
bucket       = "tfstate-calculadora-jcarvajal0810"
key          = "calculadora/terraform.tfstate"
region       = "us-east-1"
use_lockfile = true