import os
import dotenv
import json
import time
import random
from datetime import datetime, UTC
from faker import Faker
from confluent_kafka import Producer
import settings

# Load the secrets from .env files
dotenv.load_dotenv()
dotenv.load_dotenv('../.env-kafka', override=True)
dotenv.load_dotenv('../.env-pg', override=True)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', None)
if KAFKA_BOOTSTRAP_SERVERS is None:
    raise ValueError("KAFKA_BOOTSTRAP_SERVERS is not set")

# Create a Faker instance for generating fake user data
faker = Faker()

# Kafka producer configuration
producer_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "security.protocol": "SSL",
    "ssl.ca.location": settings.SSL_CA_FILE,
    "ssl.certificate.location": settings.SSL_CERT_FILE,
    "ssl.key.location": settings.SSL_KEY_FILE,
    "client.id": "clickstream-producer",
}

# Initialize Kafka producer
producer = Producer(producer_conf)

# Create a set of sessions, so that these aren't all random and we
# can aggregate some stats based on session
SESSION_IDS = [faker.uuid4() for _ in range(random.randint(5, 15))]

# Callback function for delivery report
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Generate random clickstream event
def generate_click_event():
    site = random.choice(settings.SITES)
    page = random.choice(settings.PAGES)
    event = {
        "user_id": faker.uuid4(),
        "session_id": random.choice(SESSION_IDS),
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": random.choice(["page_view", "button_click", "purchase", "search"]),
        "page_url": f"{site}{page}",
        "referrer_url": faker.url(),
        "user_agent": faker.user_agent(),
        "ip_address": faker.ipv4(),
        "device": random.choice(["mobile", "desktop", "tablet"]),
    }
    return event

# Send events to Kafka
def produce_events(num_events=100, interval:float=1):
    try:
        for _ in range(num_events):
            print("click")
            event = generate_click_event()
            event_json = json.dumps(event)
            producer.produce(
                settings.KAFKA_TOPIC,
                key=event["user_id"],
                value=event_json,
                callback=delivery_report
            )
            producer.poll(0)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.flush()  # Ensure all messages are sent

if __name__ == "__main__":
    print(f"Server connection: {KAFKA_BOOTSTRAP_SERVERS}")
    print("Producing clickstream data...")
    produce_events(num_events=500, interval=0.5)
