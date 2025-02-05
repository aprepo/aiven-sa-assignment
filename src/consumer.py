import os
import dotenv
import json
from confluent_kafka import Consumer, KafkaException
from clickstream_db import write_to_db
from clickstream_os import write_to_os
from clickstream_accumulator import ClickStreamAccumulator
import settings
from clickstream_db import write_session_stats_to_db

dotenv.load_dotenv()
dotenv.load_dotenv('../.env-kafka', override=True)
dotenv.load_dotenv('../.env-pg', override=True)
dotenv.load_dotenv('../.env-opensearch', override=True)

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

    # Initialize the ClickStreamAccumulator for tracking session stats
    accumulator = ClickStreamAccumulator()

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

            # Push the raw event data to PG
            write_to_db(event)

            # Push the raw event data to OpenSearch
            write_to_os(event)

            # As an example, calculate the event statistics and store them in the database
            accumulator.add_event(event)
            stats = accumulator.get_session_stats(event['session_id'])
            write_session_stats_to_db(event['session_id'], stats)
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()  # Ensure proper cleanup

if __name__ == "__main__":
    main()
