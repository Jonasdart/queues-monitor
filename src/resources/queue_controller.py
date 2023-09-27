from datetime import datetime
from typing import List, Optional
from .spec import load_spec
from resources.database import db, Query
from models.queue import QueueDefinition
import json
import logging

logging.basicConfig(level="INFO")


def load_queues_definitions() -> List[QueueDefinition]:
    queues_definitions: List[QueueDefinition] = [
        QueueDefinition(**queue) for queue in load_spec()["queues"]
    ]

    return queues_definitions


def delete_by_timestamp(timestamp: float):
    for table in [db.table(_) for _ in db.tables()]:
        table.remove(Query().timestamp <= timestamp)


def monitore(queue: QueueDefinition):
    table = db.table(queue.id)

    client = queue.provider.get_subscriber_client(queue.provider)
    pulled_messages = client.pull(
        request={
            "subscription": queue.pull,
            "max_messages": 200,
        }
    )

    messages = []
    ack_ids = []
    for message in pulled_messages.received_messages:
        message_data: dict = json.loads(message.message.data)
        message_data.update(
            {
                "id": message.ack_id,
                "delivery_attempt": message.delivery_attempt,
                "queue_id": queue.id,
            }
        )
        ack_ids.append(message_data["id"])
        if db.search(Query().id == message_data["id"]):
            continue

        logging.info("Nova Mensagem identificada")
        logging.info(message_data)

        messages.append(message_data)

    if ack_ids:
        client.acknowledge(subscription=queue.pull, ack_ids=ack_ids)

    table.insert_multiple(messages)


def group_by_parameter(sources: tuple, parameter: str, scape: Optional[str] = ""):
    grouped = {}
    for data in sources:
        try:
            grouped[data.get(parameter, data.get(scape))].append(data)
        except (KeyError, TypeError):
            grouped[data.get(parameter, data.get(scape))] = [data]

    return grouped


def group_by_timestamp(
    sources: dict, sub_key: Optional[str] = None, configs: Optional[dict] = {}
):
    grouped = []
    sources = list(sources.items())
    for group_index, data in enumerate(sources):
        for index, _ in enumerate(data[1]):
            item_title = data
            if sub_key:
                item_title = f"{data[0]}👉{_[sub_key]}"

            if "datetime" not in _:
                _["datetime"] = datetime.fromtimestamp(_["timestamp"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                if configs.get("range"):
                    try:
                        _["final_datetime"] = data[1][index + 1]["timestamp"]
                        _["final_datetime"] = datetime.fromtimestamp(
                            _["final_datetime"]
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    except IndexError:
                        try:
                            _["final_datetime"] = sources[group_index + 1][1][0][
                                "timestamp"
                            ]
                            _["final_datetime"] = datetime.fromtimestamp(
                                _["final_datetime"]
                            ).strftime("%Y-%m-%d %H:%M:%S")
                        except IndexError:
                            ...

            grouped.append(
                {
                    "content": item_title,
                    "start": _["datetime"],
                    "end": _.get("final_datetime"),
                    "id": _["id"],
                    "type": "range" if _.get("final_datetime") else "box",
                }
            )

    return grouped


def get_queue_definition_by_id(queue_id: str) -> QueueDefinition:
    for queue in load_queues_definitions():
        if queue.id == queue_id:
            return queue

    raise FileNotFoundError("Queue ID not identified")


def reprocess_message_by_id(message_id: str) -> bool:
    message = {}
    for table in [db.table(_) for _ in db.tables()]:
        try:
            message = table.search(Query().id == message_id)[0]
        except IndexError:
            ...
    if not message:
        raise FileNotFoundError("Queue Message Not Found")

    queue = get_queue_definition_by_id(message["queue_id"])

    message.pop("id")
    message.pop("delivery_attempt")
    message.pop("queue_id")

    json_data = json.dumps(message)
    json_data = json_data.encode("utf-8")

    client = queue.provider.get_publisher_client(queue.provider)
    reprocess_attributes = queue.reprocess.attributes
    future = client.publish(
        queue.reprocess.queue_endpoint, data=json_data, **reprocess_attributes
    )

    logging.debug(
        f"Sent message with result '{future.result()}' "
        f"to {queue.reprocess.queue_endpoint}."
    )
