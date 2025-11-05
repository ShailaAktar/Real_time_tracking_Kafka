from confluent_kafka import Consumer, KafkaException

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # or 'host.docker.internal:9092' if running from Docker
    'group.id': 'my-simple-group',
    'auto.offset.reset': 'earliest'  # Read from beginning if no offset
}

# Create the consumer
consumer = Consumer(conf)

# Subscribe to topic
consumer.subscribe(['crypto'])

try:
    print("Waiting for messages...\nPress Ctrl+C to exit.\n")
    while True:
        msg = consumer.poll(1.0)  # Wait up to 1 second
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        print(f"Received message: key={msg.key().decode() if msg.key() else None}, value={msg.value().decode()}")

except KeyboardInterrupt:
    print("\nInterrupted. Closing consumer...")

finally:
    consumer.close()