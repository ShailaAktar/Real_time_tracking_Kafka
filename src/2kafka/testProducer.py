

from confluent_kafka import Producer

# Set up configuration (where to send data)
conf = {
    'bootstrap.servers': 'localhost:9092'  # <-- This is where you're sending the data
}

producer = Producer(conf)

# Callback on delivery (optional)
def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered message to {msg.topic()} [{msg.partition()}]")

# Send data to topic "crypto"
producer.produce("coinbase", key="ETH", value="ETH price is 3500", callback=delivery_report)

# Wait for delivery
producer.flush()