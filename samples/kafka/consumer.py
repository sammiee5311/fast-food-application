import json
import socket

from kafka import KafkaConsumer

if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname())
    consumer = KafkaConsumer(
        "fast-food-order",
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{ip_address}:9092",
        auto_offset_reset="earliest",
    )
    print("Starting the comsumer")
    for msg in consumer:
        print(f"Registered user: {json.loads(msg.value)}")
