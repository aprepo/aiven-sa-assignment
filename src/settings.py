# Download these files from the Aiven console and set them up to certs dir
SSL_CA_FILE="../certs/ca.pem"
SSL_CERT_FILE="../certs/service.cert"
SSL_KEY_FILE="../certs/service.key"

# Kafka topic settings
KAFKA_TOPIC = "faker-clickstream"
KAFKA_GROUP_ID = "clickstream-consumer-group"

# Pages used for the fake data
PAGES = ["home.html", "admin.html", "user.html", "billing.html"]
SITES = ["https://killerapp.io/", "https://social.network.com/"]