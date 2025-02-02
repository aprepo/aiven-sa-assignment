resource "aiven_opensearch" "clickstream_opensearch" {
  project      = var.project_name
  service_name = "clickstream-opensearch"
  plan         = "startup-4"
  cloud_name   = var.cloud_name
}

resource "aiven_opensearch_user" "clickstream_opensearch_user" {
  service_name = aiven_opensearch.clickstream_opensearch.service_name
  project      = var.project_name
  username     = "clickstream"
  password     = var.clickstream_user_password
}