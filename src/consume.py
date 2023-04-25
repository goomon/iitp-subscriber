import json
import uuid
from configparser import ConfigParser
from typing import Optional

from confluent_kafka import Consumer, Message

from config.config import *
from logger.ConsumerLogger import ConsumerLogger
from schema.chest import ChestDeviceSensorRecord


logger = ConsumerLogger()


def main():
    # Configuration logs
    logger.info(f"SASL_USER={SASL_USERNAME}")
    logger.info(f"SASL_PASSWORD={SASL_PASSWORD}")
    logger.info(f"CONSUMED_TOPIC={CONSUMED_TOPIC}")
    logger.info(f"CONSUMER_GROUP_ID={CONSUMER_GROUP_ID}")

    # Load configuration file.
    config_parser = ConfigParser()
    config_parser.read("./config/client.ini")
    props: dict[str, str] = dict(config_parser["connections"])
    props["group.id"] = str(uuid.uuid4())
    props["auto.offset.reset"] = "earliest"

    # Define consumer object.
    consumer = Consumer(props)
    consumer.subscribe(["topic3"])

    try:
        while True:
            msg: Optional[Message] = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                record: ChestDeviceSensorRecord = json.loads(msg.value().decode("utf-8"))
                logger.debug(f"polling success: {record['window_size']}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
