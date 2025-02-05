# aiven-sa-assignment
### Coding assignment for Aiven SA interview

This is a solution to the Challenge 1: _Real time data pipeline_

- Terraform script to setup the Aiven resources
- Python script that will generate click stream data to Kafka
- Stream the data to a script that calculates session level metrics and write it to PSQL
  - Why not use Timescale for this? This is aggregate timeseries data after all and Aiven offers the Timescale open source add-in to PG as part of the offering. Implemented both as example.
- Stream the data to Opensearch for search and visualization

---
# Solution Design
This example showcases how to setup a real-time data pipeline using Aiven services. The pipeline consists of the following components:
- Kafka: To ingest the clickstream events
- PostgreSQL: To store the session level metrics, using the TimescaleDB extension to calculate the session level metrics
- OpenSearch: To store the clickstream events and visualize the data

To setup the services on the Aiven platform, we use Terraform to create the resources. Aiven
provides a custom Terraform provider that allows us to easily manage the services without the
need to manually create them.

The producer script generates clickstream events and sends them to the Kafka topic. 

The consumer will then pull the events from the Kafka topic and store them to the PostgreSQL database for
long term storage. The PostgreSQL has the TimescaleDB extension installed to allow for efficient
storage and querying of time-series data.

The consumer will also forward the events to the OpenSearch cluster for search and visualization. You
can access the OpenSearch dashboard to visualize the data and perform searches via the Aiven console.


## Setup resources with Terraform
Set the Terraform credentials by creating a ```terraform.tfvars``` file with the following variables:
```hcl
aiven_api_token = "<insert token here>"
project_name    = "aprepo-sa-demo"
postgresql_user = "clickstream_user"
postgresql_password = "<insert password here>"
cloud_name = "google-europe-north1" # Make sure we run all services in same region
clickstream_user_password = "<insert password here>"
```

Create the resources by running the terraform:
```bash
cd dist
terrafrom init 
terrafrom plan
terfaform apply
```

The resources are defined in the `*.tf` files in the [dist](dist) directory. The
parameters of the services are defined in the `variables.tf` file, including
the passwords for the services and the cloud region to be used. The services
are all set up in the same region to minimize latency.

:warning: Afer running the examples, remember to destroy the resources to avoid unnecessary costs. 
To clean up the resources, run:
```bash
cd dist
terraform destroy
```


### Kafka.tf 
The Kafka service is defined in the [kafka.tf](dist/kafka.tf) file. The service
will be a startup-2 plan with schema registry enabled. The Kafka service is used to ingest the clickstream events.
```
resource "aiven_kafka" "example_kafka" {
  project             = var.project_name
  service_name        = "sa-kafka"
  plan                = "startup-2"
  cloud_name          = var.cloud_name

  kafka_user_config {
    schema_registry   = true
  }
}
```

### Postgresql.tf
The PostgreSQL service is defined in the [postgresql.tf](dist/postgresql.tf) file. The service
is a startup-4 plan with the PG version 16.

This will also create the database for the clickstream events and the user to access the database. 
The schema of the database will be created in the next step using a python script.   
```
resource "aiven_pg" "clickstream_db" {
  project             = var.project_name
  service_name        = "sa-postgresql"
  plan                = "startup-4"
  cloud_name          = var.cloud_name

  pg_user_config {
    pg_version        = "16"
  }
}

# Create the db
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

```

Once the resources are created, go to Aiven console ([console.aiven.io](https://console.aiven.io/)) to confirm that the services are up and running. 

For the python scripts, set environment variables by creating a ```.env``` file with variable ```AIVEN_API_KEY``` with the API key to access the Aiven resources and the required passowords for the services. The file should have following content:
```bash
AIVEN_API_KEY="<insert token here>"

# Kafka service
KAFKA_BOOTSTRAP_SERVERS="<insert service URL here>"

# PG service
AIVEN_PG_HOST="<insert service host here from Aiven console>"
AIVEN_PG_PORT="<insert service port here from Aiven console>"
AIVEN_PG_DB_NAME = "clickstream"
AIVEN_PG_USER = "clickstream_user"
AIVEN_PG_PASSWORD = "<insert password here>"

# Opensearch service parameters
OPENSEARCH_HOST = "<insert service host here from Aiven console>"
OPENSEARCH_PORT = "<insert service port here from Aiven console>"
OPENSEARCH_USER = "clickstream"
OPENSEARCH_PASSWORD = "<insert password here>"
```

Create the PG schema by running the script:
```bash
cd dist
python create_pg_schema.py
```

The schema is defined in the [clickstream_schema.sql](dist/clickstream_schema.sql) file.
The clickstream events are stored to a ```clickstream_events``` table that is
setup as a TimescaleDB hypertable and partitioned by time. This allows us to efficiently store and query
the time-series data

## Setup kafka credentials
Download the Kafka SSL cert files from the Aiven console and save them to ```certs``` directory. This should be 3 files:
```commandline
ca.pem
service.cert
service.key
```

## Produce clickstream events
Start the producer by running:
```bash
cd src
python producer.py
```
This will generate clickstream events and send them to the Kafka topic.

## Consume clickstream events
Start the consumer by running:
```bash
cd src
python consumer.py
```
This will start to listen for the events from the Kafka topic and store them to the PostgreSQL database and to the OpenSearch cluster.

## Show the data from the PostgreSQL
Run the `summary.py` to see the resulting metrics from the PostgreSQL database.
```bash
cd src
python summary.py
```

To see the data in the OpenSearch, go to the Aiven console and click on the `clickstream-opensearch` 
OpenSearch service. You can access the Opensearch dashboard from the console to visualize the data.