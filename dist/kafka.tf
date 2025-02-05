resource "aiven_kafka" "clickstream_kafka" {
  project                   = data.aiven_project.clickstream_project.project
  service_name        = "clickstream-kafka"
  plan                        = "startup-2"
  cloud_name           = var.cloud_name

  kafka_user_config {
    schema_registry  = true
  }
}

resource "aiven_kafka_topic" "clickstream_topic" {
  project                   = data.aiven_project.clickstream_project.project
  service_name        = aiven_kafka.clickstream_kafka.service_name
  topic_name            = "clickstream"
  partitions                = 3
  replication              = 2
}