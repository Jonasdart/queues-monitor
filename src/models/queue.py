from datetime import timedelta
from enum import Enum
from typing import Dict
from pydantic import BaseModel, validator
from .providers import Providers


class RetentionType(str, Enum):
    ONLY_ACK_MESSAGES: str = "ONLY_ACK_MESSAGES"
    ONLY_NEW_MESSAGES: str = "ONLY_NEW_MESSAGES"
    ALL_MESSAGES: str = "ALL_MESSAGES"


class TimeDeltaRange(timedelta):
    def __new__(cls, days: float = ...) -> timedelta:
        return super().__new__(days, 0, 0, 0, 0, 0, 0)


class Config(BaseModel):
    frequency: str
    range: timedelta
    retentionType: RetentionType

    def __range_validator(range: int) -> timedelta:
        return timedelta(days=range)

    _range_validator = validator("range", pre=True, allow_reuse=True)(__range_validator)


class QueueReprocessDefinition(BaseModel):
    queue_endpoint: str
    attributes: Dict[str, str]


class QueueDefinition(BaseModel):
    id: str
    alias: str
    provider: Providers
    pull: str
    config: Config
    reprocess: QueueReprocessDefinition
