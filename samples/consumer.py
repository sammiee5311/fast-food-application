import json

from kafka import KafkaConsumer

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered-user",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        group_id="consumer-group-a",
    )
    print("Starting the comsumer")

    for msg in consumer:
        print(f"Registered user: {json.loads(msg.value)}")
