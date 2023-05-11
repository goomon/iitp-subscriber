import os
import uuid


class DBConfigurations:
    postgres_username = "postgres" if os.getenv("POSTGRES_USER") is None else os.getenv("POSTGRES_USER")
    postgres_password = "postgres" if os.getenv("POSTGRES_PASSWORD") is None else os.getenv("POSTGRES_PASSWORD")
    postgres_port = 5432 if os.getenv("POSTGRES_PORT") is None else os.getenv("POSTGRES_PORT")
    postgres_db = "postgres" if os.getenv("POSTGRES_DB") is None else os.getenv("POSTGRES_DB")
    postgres_host = "localhost" if os.getenv("POSTGRES_HOST") is None else os.getenv("POSTGRES_HOST")
    sql_alchemy_url = (
        f"postgresql://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    )


class KafkaConfigurations:
    # Connection options
    kafka_host = "" if os.getenv("KAFKA_HOST") is None else os.getenv("KAFKA_HOST")
    sasl_user = "" if os.getenv("SASL_USERNAME") is None else os.getenv("SASL_USERNAME")
    sasl_password = "" if os.getenv("SASL_PASSWORD") is None else os.getenv("SASL_PASSWORD")

    # Consumer options
    topic = "topic_1" if os.getenv("TOPIC") is None else os.getenv("TOPIC")
    consumer_group_id = str(uuid.uuid4()) if os.getenv("CONSUMER_GROUP_ID") is None else os.getenv("CONSUMER_GROUP_ID")
    consumer_instance_id = str(uuid.uuid4()) if os.getenv("CONSUMER_INSTANCE_ID") is None else os.getenv("CONSUMER_INSTANCE_ID")
    max_poll_interval_ms = 300000 if os.getenv("MAX_POLL_INTERVAL_MS") is None else os.getenv("MAX_POLL_INTERVAL_MS")
    max_poll_records = 500 if os.getenv("MAX_POLL_RECORDS") is None else os.getenv("MAX_POLL_RECORDS")
    processor_flush_timeout = 20 if os.getenv("FLUSH_TIMEOUT") is None else int(os.getenv("FLUSH_TIMEOUT"))


class InferenceConfiguration:
    model_path = 'model/small_model_checkpoint.joblib' if os.getenv("MODEL_PATH") is None else os.getenv("MODEL_PATH")
