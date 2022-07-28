from cmd import Cmd
from functools import reduce
from typing import IO, Any, List, Optional, Union
from uuid import uuid4
import zmq
from whatsapp.adapters.strategies import ThreadSubscriberTopicPoolAdder
from whatsapp.adapters.middleware import PubSubProxy


def callback(user, message):
    """Shows message"""
    print(f'{user}: {message}\n(Cmd) ', end='')


class ExitCmdException(Exception):
    pass


class TopicPrompt(Cmd):
    def __init__(
        self,
        completekey: str = 'tab',
        stdin: Union[IO[str], None] = None,
        stdout: Union[IO[str], None] = None,
    ) -> None:
        self._user = str(uuid4())
        self._subscriber: Optional[ThreadSubscriberTopicPoolAdder] = None
        self._ctx: Optional[zmq.Context[zmq.Socket[Any]]] = None
        self._client: Optional[zmq.Socket[Any]] = None
        super().__init__(completekey, stdin, stdout)

    def do_connect(self, address_and_ports: str):
        """Connects to an address

        Args:
            address_and_ports (str): Address and ports of the proxy connector
        """
        address, input_port, subscribe_port = address_and_ports.split(' ')
        self._subscriber = ThreadSubscriberTopicPoolAdder(
            remote_addres=address,
            server_port=int(input_port),
            topic_port=int(subscribe_port)
        )

    def do_enter_topic(self, topic: str):
        """Command to enter a topic

        Args:
            topic (str): Topic name
        """
        if self._subscriber is None:
            print('No connection available')
        else:
            self._subscriber.add(topic, callback)

    def do_serve(self, ports: str):
        """Serves the middleware

        Args:
            ports (str): Input and output port
        """
        int_ports: List[int] = list(map(int, ports.split(' ')))
        PubSubProxy(
            int_ports[0],
            int_ports[1]
        ).start()

    def do_exit_topic(self, topic: str):
        """Command to unsubscribe from topic

        Args:
            topic (str): Topic name
        """
        if self._subscriber is None:
            print('No connection available')
        else:
            self._subscriber.remove(topic)

    def do_send(self, message: str):
        """Command to send message to topic

        Args:
            message (str): Message with topic and content
        """
        if self._subscriber is None:
            print('No connection available')
        else:
            all_message = message.replace('\n', '').split(' ')
            topic = all_message[0]
            complete_message = reduce(lambda x, y: f'{x} {y}', all_message[1:])
            self._subscriber.send(topic, self._user, complete_message)

    def do_exit(self, *args):
        for thread in self._subscriber._thread_pool:
            self._subscriber.remove(thread)
        raise ExitCmdException()

    def do_set_user(self, user: str):
        """Command to configure user

        Args:
            user (str): Username
        """
        self.do_enter_topic(user)
        self._user = user
