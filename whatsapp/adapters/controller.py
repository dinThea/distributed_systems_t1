
from typing import List
from whatsapp.app.use_cases import (
    ListTopics,
    ListTopicsRequest,
    SendMessageToTopic,
    SubscribeToTopic,
    SubscribeToTopicRequest,
    TopicMessageSenderRequest,
    UnsubscribeFromTopic,
    UnsubscribeToTopicRequest,
    messageCallback
)


class MQControllerStub:
    """Stub to access connection use cases
    """

    def __init__(
        self,
        subscriber: SubscribeToTopic,
        unsubscriber: UnsubscribeFromTopic,
        sender: SendMessageToTopic,
        lister: ListTopics
    ):
        self._subscriber = subscriber
        self._unsubscriber = unsubscriber
        self._sender = sender
        self._lister = lister

    def send(self, topic: str, user: str, message: str):
        """Sends messages to topic

        Args:
            topic (str): Topic to receive message
            user (str): User sending the message
            message (str): Message in question
        """
        self._sender.send_message(
            TopicMessageSenderRequest(
                user=user,
                topic=topic,
                message=message
            )
        )

    def add(self, topic_id: str, callback: messageCallback):
        """Add user (connection) to topic, setting a callback as \
            receiver

        Args:
            topic_id (str): Topic to connect to
            callback (messageCallback): Callback to be called on message
        """
        self._subscriber.subscribe(
            SubscribeToTopicRequest(
                topic_id=topic_id,
                callback=callback
            )
        )

    def remove(self, topic_id: str):
        """Remove user from topic

        Args:
            topic_id (str): Topic to remove user from
        """
        self._unsubscriber.unsubscribe(
            UnsubscribeToTopicRequest(
                topic_id=topic_id
            )
        )

    def list(self) -> List[str]:
        """Lists topics

        Returns:
            List[str]: List of topics
        """
        return self._lister.execute(
            ListTopicsRequest()
        ).topics
