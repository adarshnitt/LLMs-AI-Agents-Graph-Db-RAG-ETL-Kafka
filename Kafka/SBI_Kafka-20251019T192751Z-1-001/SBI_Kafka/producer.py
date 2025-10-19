# i had install resp[pective libraries inside venv, plz activate it ]

import json
import uuid

from confluent_kafka import Producer


# ur producer is running in ur local computer but kafka is running in side continaer. kafka already advertise that anyone wants to conncet kafka could cinnect via current active ip addrss: 172.26.80.1:9092

# interation btwm continerrunning kafka and our producer running in my local vuia this ip
producer_config = {
    "bootstrap.servers": "192.168.1.75:9092" # where kafka is accesible, refer this var: KAFKA_ADVERTISED_LISTENERS in docker-compose.yaml
}

producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered {msg.value().decode("utf-8")}")
        print(f"Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")

# offset will start from 0, nth offset is nth event and dtype storeage is log formaticaly
order = {
    "order_id": str(uuid.uuid4()),
    "user": "Adarsh1",
    "item": "who moved my cheese",
    "quantity": "sixth order"
}

value = json.dumps(order).encode("utf-8")
print("first kafka producer is going to start producing data to topic adarsh_orders")
producer.produce(
    topic="adarsh_orders",
    value=value,
    callback=delivery_report # after execution, callback will run to check observationclear
)

# flush will send data which are in quie/asyn before closing process.
producer.flush()
