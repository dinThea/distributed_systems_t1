from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List

messageCallback = Callable[[str, str], None]


@dataclass
class SubscribeToTopicRequest:
    """Request to subscribe to topic
    """
    topic_id: str
    callback: messageCallback


@dataclass
class UnsubscribeToTopicRequest:
    """Request to subscribe to topic
    """
    topic_id: str


class TopicRemover(ABC):
    """Interface for the strategy to unsubscribe from topic"""
    @abstractmethod
    def remove(self, topic_id: str):
        ...


class TopicMessageSender(ABC):
    """Interface for the strategy to send messages to topic
    """
    @abstractmethod
    def send(self, topic: str, user: str, message: str):
        ...


class TopicAdder(ABC):
    """Interface for the strategy to subscribe from topic"""
    @abstractmethod
    def add(self, topic_id: str, callback: messageCallback):
        ...


class SubscribeToTopic():
    """Subscribe to topic use case
    """

    def __init__(
            self,
            topic_pool_manager_adder: TopicAdder
    ):
        self._topic_pool_manager_adder = topic_pool_manager_adder

    def subscribe(self, request: SubscribeToTopicRequest):
        self._topic_pool_manager_adder.add(
            topic_id=request.topic_id,
            callback=request.callback
        )


@dataclass
class ListTopicsRequest:
    """List topics"""
    ...


@dataclass
class ListTopicsResponse:
    """List of topics"""
    topics: List[str]


class TopicLister(ABC):
    """List topics"""
    @abstractmethod
    def list(self) -> List[str]:
        ...


class ListTopics:
    def __init__(self, topic_lister: TopicLister):
        self._topic_lister = topic_lister

    def execute(self, _: ListTopicsRequest):
        return ListTopicsResponse(topics=self._topic_lister.list())


@dataclass
class TopicMessageSenderRequest:
    user: str
    topic: str
    message: str


class SendMessageToTopic():
    """Send message to topic use case
    """

    def __init__(
        self,
        topic_message_sender: TopicMessageSender
    ):
        self._topic_message_sender = topic_message_sender

    def send_message(self, request: TopicMessageSenderRequest):
        self._topic_message_sender.send(
            topic=request.topic,
            user=request.user,
            message=request.message
        )


class UnsubscribeFromTopic():
    """Usubscribe from topic use case
    """

    def __init__(
        self,
        topic_pool_manager_remover: TopicRemover
    ):
        self._topic_pool_manager_remover = topic_pool_manager_remover

    def unsubscribe(self, request: UnsubscribeToTopicRequest):
        self._topic_pool_manager_remover.remove(
            topic_id=request.topic_id
        )
