from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

messageCallback = Callable[[str, str], None]


@dataclass
class SubscribeToTopicRequest:
    topic_id: str
    callback: messageCallback


@dataclass
class UnsubscribeToTopicRequest:
    topic_id: str


class TopicPoolManagerRemover(ABC):
    @abstractmethod
    def remove(self, topic_id: str):
        ...


class TopicPoolManagerAdder(ABC):
    @abstractmethod
    def add(self, topic_id: str, callback: messageCallback):
        ...


class SubscribeToTopic():
    def __init__(
            self,
            topic_pool_manager_adder: TopicPoolManagerAdder
    ):
        self._topic_pool_manager_adder = topic_pool_manager_adder

    def subscribe(self, request: SubscribeToTopicRequest):
        self._topic_pool_manager_adder.add(
            topic_id=request.topic_id,
            callback=request.callback
        )


class UnsubscribeFromTopic():
    def __init__(
        self,
        topic_pool_manager_remover: TopicPoolManagerRemover
    ):
        self._topic_pool_manager_remover = topic_pool_manager_remover

    def unsubscribe(self, request: UnsubscribeToTopicRequest):
        self._topic_pool_manager_remover.remove(
            topic_id=request.topic_id
        )
