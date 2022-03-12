from kafka import KafkaConsumer

from utils.log import logger


def get_consumer(topic: str, ip_address: str, port: int) -> KafkaConsumer:
    logger.info("Starting the comsumer")
    consumer = KafkaConsumer(
        topic,
        security_protocol="PLAINTEXT",
        bootstrap_servers=f"{ip_address}:{port}",
        auto_offset_reset="earliest",
    )

    return consumer
