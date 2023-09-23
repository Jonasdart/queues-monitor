from time import sleep
from resources.queue_controller import monitore, queues_definitions
from dotenv import load_dotenv

load_dotenv()


def start_consume():
    for queue in queues_definitions:
        monitore(queue)

if __name__ == "__main__":
    while True:
        start_consume()
        sleep(1)