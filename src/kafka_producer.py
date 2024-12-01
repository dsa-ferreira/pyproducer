from confluent_kafka import Producer

class KafkaProducer:

    def __init__(self, kafka_server: str, topic: str, wait: bool = False):
        conf = {
            'bootstrap.servers': kafka_server,
            'default.topic.config': {'api.version.request': False},
#            'log_level': 0
        }

        self.producer = Producer(conf)
        self.topic = topic
        self.wait = wait

    def send(self, message: str, topic: str = ""):
        if topic == "" and self.topic == "":
            raise Exception("No topic defined")
        self.producer.produce(
            self.topic if topic == "" else topic,
            key="1",
            value=message.encode('UTF-8'))
        self.producer.flush()
