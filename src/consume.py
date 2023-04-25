import json
import uuid
from configparser import ConfigParser
from typing import Optional

from confluent_kafka import Consumer, Message

from schema.chest import ChestDeviceSensorRecord


def main():
    config_parser = ConfigParser()
    config_parser.read("./config/client.ini")
    props: dict[str, str] = dict(config_parser["connections"])
    props["group.id"] = str(uuid.uuid4())
    props["auto.offset.reset"] = "earliest"

    consumer = Consumer(props)
    consumer.subscribe(["topic3"])

    try:
        while True:
            msg: Optional[Message] = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                record: ChestDeviceSensorRecord = json.loads(msg.value().decode("utf-8"))
                print("window size:", record["window_size"])
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
