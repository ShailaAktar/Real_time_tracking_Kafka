from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

# Explicitly assign to partition 2
from confluent_kafka import TopicPartition
consumer.assign([TopicPartition("coinbase", 2)])

print("⏳ Waiting for ETH messages in partition 2...\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"⚠️ Error: {msg.error()}")
            continue

        print(f"📨 Received: {msg.value().decode()} (key={msg.key().decode()})")
        # 👉 This is where you'd send it to a user

except KeyboardInterrupt:
    print("Stopping...")
finally:
    consumer.close()