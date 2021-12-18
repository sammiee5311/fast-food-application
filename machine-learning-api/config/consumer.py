from kafka import KafkaConsumer


def get_consumer(topic: str, ip_address: str, port: int) -> KafkaConsumer:
    consumer = KafkaConsumer(
        topic,
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{ip_address}:{port}",
        auto_offset_reset="earliest",
    )

    return consumer
