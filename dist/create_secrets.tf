# This tf script pulls the settings from the Aiven services
# and creates the .env file with the secrets, so that the user
# does not have to go to Aiven console for them.

# SSL cert for the project
resource "local_file" "ca_cert" {
  content  = data.aiven_project.clickstream_project.ca_cert
  filename = "${path.module}/../certs/ca.pem"
}

# Store Kafka Service URI
resource "local_file" "dotenv-kafka" {
  content  = <<-EOT
    KAFKA_BOOTSTRAP_SERVERS = "${aiven_kafka.clickstream_kafka.service_uri}"
  EOT
  filename = "${path.module}/../.env-kafka"
}

# Store Kafka Access Certificate
resource "local_file" "kafka_access_cert" {
  content  = aiven_kafka.clickstream_kafka.kafka[0].access_cert
  filename = "${path.module}/../certs/service.cert"
}

# Store Kafka Access Key
resource "local_file" "kafka_access_key" {
  content  = aiven_kafka.clickstream_kafka.kafka[0].access_key
  filename = "${path.module}/../certs/service.key"
}

# Store the Postgres Service URI
resource "local_file" "pg_dotenv" {
  content = <<-EOT
    AIVEN_PG_URI="${aiven_pg.clickstream_db.service_uri}"
    AIVEN_PG_HOST="${aiven_pg.clickstream_db.service_host}"
    AIVEN_PG_PORT=${aiven_pg.clickstream_db.service_port}
    AIVEN_PG_DB_NAME = "clickstream"
    AIVEN_PG_USER = "${aiven_pg.clickstream_db.service_username}"
    AIVEN_PG_PASSWORD = "${aiven_pg.clickstream_db.service_password}"
    "
  EOT
  filename = "${path.module}/../.env-pg"
}

# Store the OpenSearch Service parameters
resource "local_file" "opensearch_dotenv" {
  content = <<-EOT
      OPENSEARCH_HOST = "${aiven_opensearch.clickstream_opensearch.service_host}"
      OPENSEARCH_PORT = "${aiven_opensearch.clickstream_opensearch.service_port}"
      OPENSEARCH_USER = "${aiven_opensearch.clickstream_opensearch.service_username}"
      OPENSEARCH_PASSWORD = "${aiven_opensearch.clickstream_opensearch.service_password}"
  EOT
  filename = "${path.module}/../.env-opensearch"
}