# aiven-sa-assignment
Coding assignment for Aiven SA interview

This is a solution to the Challenge 1: _Real time data pipeline_

- Terraform script to setup the Aiven resources
- Python script that will generate click stream data to Kafka
- Stream the data to a script that calculates session level metrics and write it to PSQL
  - Why not use Timescale for this? This is agregate timeseries data, after all and Aiven offers the Timescale open source add-in to PG as part of the offering.
- Stream the data to Opensearch for search and visualization

## Setup resources with Terraform
- Set environment variables by creating a ```.env``` file with variable ```AIVEN_API_KEY``` with the API key to access the Aiven resources.
- Export the env vars by running:  ```source set_env.sh```
- Create the resources by running the terraform:
```bash
cd dist
terrafrom init 
terrafrom plan
terfaform apply
```
- Create the PG schema by running the script:
```bash
cd dist
python create_pg_schema.py
```

## Setup kafka credentials
- Download the Kafka SSL cert files from the Aiven console and save them to ```certs``` directory. This should be 3 files:
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

## Consume clickstream events
Start the consumer by running:
```bash
cd src
python consumer.py
```