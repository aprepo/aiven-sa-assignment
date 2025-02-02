# aiven-sa-assignment
Coding assignment for Aiven SA interview

This is a solution to the Challenge 1: _Real time data pipeline_

- Terraform script to setup the Aiven resources
- Python script that will generate click stream data to Kafka
- Stream the data to a script that calculates session level metrics and write it to PSQL
  - Why not use Timescale for this? This is agregate timeseries data, after all and Aiven offers the Timescale open source add-in to PG as part of the offering.
- Stream the data to Opensearch for search and visualization

## Setup
1. Set environment variables by creating a ```.env``` file with variable ```AIVEN_API_KEY``` with the API key to access the Aiven resources.
2. Export the env vars by running:  ```source set_env.sh```
3. Create the resources by running the terraform:
```bash
cd dist
terrafrom init 
terrafrom plan

```