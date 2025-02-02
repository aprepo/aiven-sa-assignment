resource "aiven_pg" "clickstream_db" {
  project             = var.project_name
  service_name        = "sa-postgresql"
  plan                = "startup-4"
  cloud_name          = "google-europe-north1"

  pg_user_config {
    pg_version        = "16"
  }
}

# Create the db and tables
resource "aiven_pg_database" "clickstream_db" {
  project      = var.project_name
  service_name = aiven_pg.clickstream_db.service_name
  database_name = "clickstream"
}

# User
resource "aiven_pg_user" "clickstream_user" {
  project      = var.project_name
  service_name = aiven_pg.clickstream_db.service_name
  username     = var.postgresql_user
  password     = var.postgresql_password
}

