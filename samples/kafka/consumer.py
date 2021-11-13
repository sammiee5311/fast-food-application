import json

from kafka import KafkaConsumer

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered-user",
        security_protocol="PLAINTEXT",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
    )
    print("Starting the comsumer")
    for msg in consumer:
        print(f"Registered user: {json.loads(msg.value)}")
