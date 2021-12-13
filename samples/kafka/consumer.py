import json
import socket

from kafka import KafkaConsumer

IP_ADDRESS = socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "fast-food-order",
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{IP_ADDRESS}:9092",
        auto_offset_reset="earliest",
    )
    print("Starting the comsumer")
    for msg in consumer:
        print(f"Registered user: {json.loads(msg.value)}")
