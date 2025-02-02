import time
from kafka import KafkaProducer

TOPIC_NAME = "faker-clickstream"

producer = KafkaProducer(
    bootstrap_servers=f"sa-kafka-aprepo-sa-demo.j.aivencloud.com:24847",
    security_protocol="SSL",
    ssl_cafile="../cert/ca.pem",
    ssl_certfile="../cert/service.cert",
    ssl_keyfile="../cert/service.key",
)

for i in range(100):
    message = f"Hello from Python using SSL {i + 1}!"
    producer.send(TOPIC_NAME, message.encode('utf-8'))
    print(f"Message sent: {message}")
    time.sleep(1)

producer.close()