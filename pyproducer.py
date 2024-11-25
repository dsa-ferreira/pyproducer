import json
from time import sleep
import argparse
from src.utils.printer import print_user_message
from src.kafka_producer import KafkaProducer as Producer
from src.utils.reflection import find_event_models


def _options():
    parser = argparse.ArgumentParser(
                    prog='PyProducer',
                    description='Python CLI for generating and producing kafka events')
    parser.add_argument("-e", "--event-count",
                         type=int,
                         default=1,
                         help="number of events that will be produced")
    parser.add_argument("-s", "--batch-sleep",
                         type=int,
                         default=1,
                         help="sleep time between batches")
    parser.add_argument("-d", "--delta",
                         dest="delta",
                         type=int,
                         help="timespan for producing the events")
    parser.add_argument("-b", "--broker",
                         dest="broker",
                         default="localhost:9092",
                         help="the kafka broker host")
    parser.add_argument("-t", "--topic",
                         dest="topic",
                         help="kafka topic for producing the events")
    parser.add_argument("-i", "--input",
                         dest="input",
                         default="models",
                         help="kafka topic for producing the events")


    return parser.parse_args()

def _calculate_batch_count(delta, batch_sleep):
    return delta / batch_sleep if delta is not None and delta != 0 else 1

def pyproducer(event_count = 1, batch_sleep = 1, delta = 0, broker = "localhost:9092", topic = "", input = "models"):
    events = find_event_models(input)

    producer = Producer(broker, topic)

    batch_count = _calculate_batch_count(delta, batch_sleep)
    events_per_batch = event_count / batch_count

    for _ in range(int(batch_count)):
        for i in range(int(events_per_batch)):
            event = events[i%len(events)]()
            payload = json.dumps(event.apply())
            producer.send(payload, event.topic)

        sleep(batch_sleep)



def _main():
    options = _options()
    pyproducer(**vars(options))

if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        print_user_message("Why the heck are we stopping?!")
