export $(grep -v '^#' .env | xargs)
export TF_VAR_aiven_api_token=$AIVEN_API_TOKEN