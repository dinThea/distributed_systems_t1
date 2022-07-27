from dataclasses import dataclass
import functools
from threading import Thread
from typing import (
    List,
    Mapping
)
import zmq
from whatsapp.app.use_cases import TopicPoolManagerAdder, TopicPoolManagerRemover, messageCallback


def subscriber_thread(
    address: str,
    port: int,
    topic: str,
    callback: messageCallback,
    control: bool
):
    """Thread to call an subscribe to an thread

    Args:
        port (int): Port to be used in the connection
        topic (str): Topic to listen
        callback (messageCallback): Callback to be called on message
    """
    ctx = zmq.Context.instance()

    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect(f"{address}:{port}")
    subscriber.setsockopt(zmq.SUBSCRIBE, topic.encode('utf-8'))

    while control:
        try:
            msg: List[bytes] = subscriber.recv_multipart()
            user, message = msg[0].decode('utf-8').replace(f'{topic}.', '').split('.')
            callback(user, message)
        except zmq.ZMQError as exception:
            if exception.errno == zmq.ETERM:
                break
            else:
                raise


@dataclass
class Topic:
    """Strategy topic data class
    """
    thread: Thread
    control: bool


class ThreadSubscriberTopicPoolAdder(
    TopicPoolManagerAdder,
    TopicPoolManagerRemover
):
    """Implementation of the topic functions
    """

    def __init__(
        self,
        remote_addres: str,
        server_port: int,
        topic_port: int
    ):
        self._thread_pool: Mapping[str, Topic] = {}
        self._address = remote_addres
        self._server_port = server_port
        self._topic_port = topic_port
        self._ctx = zmq.Context.instance()
        self._client = self._ctx.socket(zmq.REQ)
        self._client.connect(f"{self._address}:{self._server_port}")

    def send(self, topic: str, user: str, message: str):

        self._client.send(f'{topic}.{user}.{message}'.encode('utf-8'))
        _ = self._client.recv()

    def add(self, topic_id: str, callback: messageCallback):

        control = True
        self._thread_pool[topic_id] = Topic(  # type: ignore
            thread=Thread(
                target=functools.partial(
                    subscriber_thread,
                    self._address,
                    self._topic_port,
                    topic_id,
                    callback,
                    control
                )
            ),
            control=control
        )
        self._thread_pool[topic_id].thread.start()

    def remove(self, topic_id: str):
        self._thread_pool[topic_id].control = False
