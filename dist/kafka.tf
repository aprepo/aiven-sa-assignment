resource "aiven_kafka" "example_kafka" {
  project             = var.project_name
  service_name        = "sa-kafka"
  plan                = "startup-2"
  cloud_name          = "aws-us-east-1"

  kafka_user_config {
    #kafka_version     = "3"
    schema_registry   = true
    #access_control    = true
  }
}