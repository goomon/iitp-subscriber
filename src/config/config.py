import os

# Connection options
SASL_USERNAME = "" if os.getenv("SASL_USERNAME") else os.getenv("SASL_USERNAME")
SASL_PASSWORD = "" if os.getenv("SASL_PASSWORD") else os.getenv("SASL_PASSWORD")

# Consumer options
CONSUMED_TOPIC = "" if os.getenv("TOPIC") else os.getenv("TOPIC")
CONSUMER_GROUP_ID = "" if os.getenv("CONSUMER_GROUP_ID") else os.getenv("CONSUMER_GROUP_ID")
