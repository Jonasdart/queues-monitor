from enum import Enum
from typing import Optional, Union
from google.cloud import pubsub_v1


class Providers(str, Enum):
    GCP_PUBSUB: str = "GCP-PUBSUB"
    GCP_PUBSUB_LITE: str = "GCP-PUBSUB-LITE"
    AWS_SQS: str = "AWS-SQS"

    @classmethod
    def get_subscriber_client(
        cls, provider, auth_client: Optional[str] = None
    ) -> Union[pubsub_v1.SubscriberClient, None]:
        clients = {
            cls.GCP_PUBSUB: pubsub_v1.SubscriberClient,
            cls.GCP_PUBSUB_LITE: pubsub_v1.SubscriberClient,
            cls.AWS_SQS: None,
        }
        return clients[provider]()
    

    @classmethod
    def get_publisher_client(
        cls, provider, auth_client: Optional[str] = None
    ) -> Union[pubsub_v1.PublisherClient, None]:
        clients = {
            cls.GCP_PUBSUB: pubsub_v1.PublisherClient,
            cls.GCP_PUBSUB_LITE: pubsub_v1.PublisherClient,
            cls.AWS_SQS: None,
        }
        return clients[provider]()
