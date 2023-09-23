from datetime import datetime, timedelta
from time import sleep
from resources.queue_controller import delete_by_timestamp, monitore, load_queues_definitions
from dotenv import load_dotenv

load_dotenv()


def start_consume():
    for queue in load_queues_definitions():
        monitore(queue)


def clean_oldest_queues():
    for queue in load_queues_definitions():
        range = datetime.now() - queue.config.range
        delete_by_timestamp(range.timestamp())

if __name__ == "__main__":
    while True:
        start_consume()
        clean_oldest_queues()
        sleep(1)