resource "aiven_pg" "example_pg" {
  project             = var.project_name
  service_name        = "sa-postgresql"
  plan                = "business-4"
  cloud_name          = "aws-us-east-1"

  pg_user_config {
    pg_version        = "14"
  }
}