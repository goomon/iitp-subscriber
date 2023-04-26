import os

# Connection options
KAFKA_HOST = "" if os.getenv("KAFKA_HOST") is None else os.getenv("KAFKA_HOST")
SASL_USERNAME = "" if os.getenv("SASL_USERNAME") is None else os.getenv("SASL_USERNAME")
SASL_PASSWORD = "" if os.getenv("SASL_PASSWORD") is None else os.getenv("SASL_PASSWORD")

# Consumer options
TOPIC = "" if os.getenv("TOPIC") is None else os.getenv("TOPIC")
CONSUMER_GROUP_ID = "" if os.getenv("CONSUMER_GROUP_ID") is None else os.getenv("CONSUMER_GROUP_ID")
CONSUMER_INSTANCE_ID = "" if os.getenv("CONSUMER_INSTANCE_ID") is None else os.getenv("CONSUMER_INSTANCE_ID")
MAX_POLL_MS = "" if os.getenv("MAX_POLL_MS") is None else os.getenv("MAX_POLL_MS")
MAX_POLL_RECORDS = "" if os.getenv("MAX_POLL_RECORDS") is None else os.getenv("MAX_POLL_RECORDS")
POLL_RECORDS = "" if os.getenv("POLL_RECORDS") is None else os.getenv("POLL_RECORDS")
