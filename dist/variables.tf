variable "aiven_api_token" {
  description = "Aiven token"
  type        = string
}

variable "project_name" {
  description = "Aiven console project name"
  type        = string
}

variable "postgresql_user" {
  description = "Postgresql username"
  type        = string
}

variable "postgresql_password" {
  description = "Postgresql password"
  type        = string
  sensitive   = true
}

variable "cloud_name" {
  description = "Cloud provider and region"
  type        = string
}

variable "clickstream_user_password" {
  description = "Clickstream user password"
  type = string
  sensitive = true
}
