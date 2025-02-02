import os
import dotenv
import json
from confluent_kafka import Consumer, KafkaException
import settings

dotenv.load_dotenv()

# Kafka Consumer configuration
consumer_conf = {
    "bootstrap.servers": os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
    "security.protocol": "SSL",
    "ssl.ca.location": settings.SSL_CA_FILE,
    "ssl.certificate.location": settings.SSL_CERT_FILE,
    "ssl.key.location": settings.SSL_KEY_FILE,
    "group.id": settings.KAFKA_GROUP_ID,
    "auto.offset.reset": "earliest",  # Start from the beginning if no offset is stored
}

def main():
    # Create Kafka Consumer
    consumer = Consumer(consumer_conf)
    consumer.subscribe([settings.KAFKA_TOPIC])

    print(f"Listening for messages on topic: {settings.KAFKA_TOPIC}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Wait for message
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            # Decode JSON message
            event = json.loads(msg.value().decode("utf-8"))
            print(f"Received event: {event}")

    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()  # Ensure proper cleanup

if __name__ == "__main__":
    main()
