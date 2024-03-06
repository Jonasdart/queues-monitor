from datetime import datetime
from time import sleep
from resources.queue_controller import (
    delete_by_timestamp,
    monitore,
    load_queues_definitions,
)


def start_consume():
    for queue in load_queues_definitions():
        monitore(queue)


def clean_oldest_queues():
    for queue in load_queues_definitions():
        range = datetime.now() - queue.config.range
        delete_by_timestamp(range.timestamp())


if __name__ == "__main__":
    while True:
        clean_oldest_queues()
        start_consume()
        sleep(1)
