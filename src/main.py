import json
import time
from configparser import ConfigParser
from typing import Optional

from confluent_kafka import Consumer, Message

from db import models
from db.models import Base
from db.database import get_context_db, engine
from logger.ConsumerLogger import ConsumerLogger
from schema.chest import ChestDeviceSensorRecord
from configurations import KafkaConfigurations

logger = ConsumerLogger()


def main():
    # Configuration logs
    logger.info(f"KAFKA_HOST={KafkaConfigurations.kafka_host}")
    logger.info(f"SASL_USER={KafkaConfigurations.sasl_user}")
    logger.info(f"SASL_PASSWORD={KafkaConfigurations.sasl_user}")
    logger.info(f"CONSUMED_TOPIC={KafkaConfigurations.topic}")
    logger.info(f"CONSUMER_GROUP_ID={KafkaConfigurations.consumer_group_id}")
    logger.info(f"CONSUMER_INSTANCE_ID={KafkaConfigurations.consumer_instance_id}")
    logger.info(f"MAX_POLL_INTERVAL_MS={KafkaConfigurations.max_poll_interval_ms}")
    logger.info(f"MAX_POLL_RECORDS={KafkaConfigurations.max_poll_records}")
    logger.info(f"FLUSH_TIMEOUT={KafkaConfigurations.processor_flush_timeout}")

    # Load configuration file.
    config_parser = ConfigParser()
    config_parser.read("connections.ini")
    props: dict[str, str] = dict(config_parser["connections"])
    props["group.id"] = KafkaConfigurations.consumer_group_id
    props["group.instance.id"] = KafkaConfigurations.consumer_instance_id
    props["auto.offset.reset"] = "latest"

    # Creating database
    Base.metadata.create_all(engine)

    # Define consumer object.
    consumer = Consumer(props)
    consumer.subscribe([KafkaConfigurations.topic])

    # Database sessions
    last_polled = time.time()
    with get_context_db() as db:
        try:
            while True:
                if time.time() - last_polled >= 60:
                    logger.debug("poll timeout")
                    break
                msg: Optional[Message] = consumer.poll(1.0)
                if msg is not None and msg.error() is None:
                    current_time = int(time.time() * 1000)
                    record: ChestDeviceSensorRecord = json.loads(msg.value().decode("utf-8"))
                    data = models.EndRecord(
                        connection_id=record["connection_id"],
                        timestamp=int(time.time() * 1000),
                    )
                    db.add(data)
                    logger.debug(f"[success] partition: {record['connection_id']}, current_time: {current_time}")
                    last_polled = time.time()
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()
        db.commit()


if __name__ == "__main__":
    main()
