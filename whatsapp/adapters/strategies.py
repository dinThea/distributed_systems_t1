"""Defines strategies to connect to a proxy"""
from dataclasses import dataclass
from queue import Queue, Empty
import functools
from threading import Thread
from time import sleep
from typing import (
    List,
    Mapping
)
import re
import zmq
from whatsapp.app.use_cases import TopicPoolManagerAdder, TopicPoolManagerRemover, messageCallback


def subscriber_thread(
    address: str,
    port: int,
    topic: str,
    callback: messageCallback,
    control: Queue
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
    data = None
    while data is None:
        try:
            msg: List[bytes] = subscriber.recv_multipart(flags=zmq.NOBLOCK)
            decoded = msg[0].decode('utf-8')
            user, message = re.sub('^'+topic+r'\.', '', decoded).split('.')
            callback(user, message)
        except zmq.ZMQError as _:
            sleep(.01)
        try:
            data = control.get(False)
        except Empty:
            data = None
        except Exception as _:
            continue


@dataclass
class Topic:
    """Strategy topic data class
    """
    thread: Thread
    control: Queue


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
        self._client = self._ctx.socket(zmq.PUB)
        self._client.connect(f"{self._address}:{self._server_port}")

    def send(self, topic: str, user: str, message: str):

        self._client.send(f'{topic}.{user}.{message}'.encode('utf-8'))

    def add(self, topic_id: str, callback: messageCallback):

        control: Queue = Queue()
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
        self._thread_pool[topic_id].control.put('control')
