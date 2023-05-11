import json
import random
import time
import warnings
from configparser import ConfigParser
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from confluent_kafka import Consumer, Message

from configurations import KafkaConfigurations, InferenceConfiguration
from db import models
from db.database import get_context_db, engine
from db.models import Base
from logger.ConsumerLogger import ConsumerLogger
from schema.chest import ChestDeviceSensorRecord, ChestDeviceSensorValue

logger = ConsumerLogger()


def extract_features(record: ChestDeviceSensorRecord) -> pd.DataFrame:
    feature_dict = {
        "user_id": record["user_id"],
        "timestamp": record["timestamp"],
        "label": record["label"],
    }

    columns = vars(ChestDeviceSensorValue).get("__annotations__").keys()
    for col in columns:
        for i in range(record["window_size"]):
            if i == 0:
                if col == "chest_acc":
                    values = [random.randint(0, 1000) for _ in range(700)]
                    # TODO: handle three values (x, y, z) in chest_acc
                else:
                    values = record["value"][i][col]["value"]
            else:
                if col == "chest_acc":
                    values.extend([random.randint(0, 1000) for _ in range(700)])
                else:
                    values.extend(record["value"][i][col]["value"])

            logger.debug(f"length of streamed data::: {len(values)}")
            feature_dict[f"{col}_mean"] = np.mean(values)
            feature_dict[f'{col}_std'] = np.std(values)
            feature_dict[f"{col}_max"] = np.max(values)
            feature_dict[f'{col}_min'] = np.min(values)

    _feature_df = pd.DataFrame([feature_dict])
    logger.debug(f"Extracted features: \n{_feature_df.head()}")
    return _feature_df


def predict_stress(feature_df: pd.DataFrame) -> int:
    # Fetch model checkpoints
    model = joblib.load(InferenceConfiguration.model_path)
    logger.debug("model is successfully loaded.")

    columns = feature_df.columns.tolist()
    columns = columns[3:]
    X = feature_df[columns]
    y = feature_df["label"]
    X, y = X.values, y.values
    predicted_y = model.predict(X)
    logger.debug(f"predicted_y: {predicted_y}, y: {y}, are they same? {predicted_y.item() == y}")
    return predicted_y.item()


def main():
    # Ignore warnings from depreciation.
    warnings.simplefilter("ignore")

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

    logger.info(f"MODEL_PATH={InferenceConfiguration.model_path}")

    # Load configuration file.
    config_parser = ConfigParser()
    config_parser.read("connections.ini")
    props: dict[str, str] = dict(config_parser["connections"])
    props["group.id"] = KafkaConfigurations.consumer_group_id
    props["group.instance.id"] = KafkaConfigurations.consumer_instance_id
    # props["auto.offset.reset"] = "latest"
    props["auto.offset.reset"] = "earliest"

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
                # This logic is just for testing. If there are any records to fetch, this process will stop.
                if time.time() - last_polled >= 60:
                    logger.debug("poll timeout")
                    break

                msg: Optional[Message] = consumer.poll(1.0)
                if msg is not None and msg.error() is None:
                    current_time = int(time.time() * 1000)
                    # Update last_polled time to track elapsed time.
                    last_polled = time.time()

                    record: ChestDeviceSensorRecord = json.loads(msg.value().decode("utf-8"))
                    # TODO: it should be removed.
                    record["label"] = 0

                    # Prediction.
                    feature_df: pd.DataFrame = extract_features(record)
                    predicted_stress_result = predict_stress(feature_df)
                    logger.info(f"Predicted stress result is: {predicted_stress_result}")
                    # TODO: inference_time should be included in database columns.
                    inference_time = int(time.time() * 1000)

                    # Add fetch time to Database sessions.
                    data = models.EndRecord(
                        connection_id=record["connection_id"],
                        timestamp=current_time,
                        # TODO: inference_time should be included in database columns.
                        # inference_timestamp=inference_time,
                    )
                    db.add(data)
                    logger.debug(f"[success] connection_id: {record['connection_id']}, current_time: {current_time}")
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

        # Finally, all data in DB transaction is inserted to database.
        # Because of a performance issue, the transaction is committed right before process stops is
        db.commit()


if __name__ == "__main__":
    main()
