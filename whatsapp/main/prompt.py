from cmd import Cmd
from functools import reduce
from typing import IO, List, Union
from uuid import uuid4
from whatsapp.adapters.controller import MQControllerStub
from whatsapp.adapters.strategies import ZmqTopicStrategies
from whatsapp.adapters.middleware import PubSubProxy
from whatsapp.app.use_cases import ListTopics, SendMessageToTopic, SubscribeToTopic, UnsubscribeFromTopic


def callback(user, message):
    """Shows message"""
    print(f'{user}: {message}\n(Cmd) ', end='')


class ExitCmdException(Exception):
    pass


def create_controller(
    remote_addr: str,
    server_port: int,
    topic_port: int
):
    """Concrete factory to create the server stub

    Args:
        remote_addr (str): Remote address of server
        server_port (int): Remote port to send messages
        topic_port (int): Remote port to subscribe
    """

    strategies = ZmqTopicStrategies(
        remote_addres=remote_addr,
        server_port=server_port,
        topic_port=topic_port
    )

    return MQControllerStub(
        subscriber=SubscribeToTopic(
            topic_pool_manager_adder=strategies
        ),
        unsubscriber=UnsubscribeFromTopic(
            topic_pool_manager_remover=strategies
        ),
        sender=SendMessageToTopic(
            topic_message_sender=strategies
        ),
        lister=ListTopics(
            topic_lister=strategies
        )
    )


class TopicPrompt(Cmd):
    def __init__(
        self,
        completekey: str = 'tab',
        stdin: Union[IO[str], None] = None,
        stdout: Union[IO[str], None] = None,
    ) -> None:
        self._user = str(uuid4())
        self._controller = None
        super().__init__(completekey, stdin, stdout)

    def do_connect(self, address_and_ports: str):
        """Connects to an address

        Args:
            address_and_ports (str): Address and ports of the proxy connector
        """
        address, input_port, subscribe_port = address_and_ports.split(' ')
        self._controller = create_controller(address, int(input_port), int(subscribe_port))

    def do_enter_topic(self, topic: str):
        """Command to enter a topic

        Args:
            topic (str): Topic name
        """
        if self._controller is None:
            print('No connection available')
        else:
            self._controller.add(topic, callback)

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
        if self._controller is None:
            print('No connection available')
        else:
            self._controller.remove(topic)

    def do_send(self, message: str):
        """Command to send message to topic

        Args:
            message (str): Message with topic and content
        """
        if self._controller is None:
            print('No connection available')
        else:
            all_message = message.replace('\n', '').split(' ')
            topic = all_message[0]
            complete_message = reduce(lambda x, y: f'{x} {y}', all_message[1:])
            self._controller.send(topic, self._user, complete_message)

    def do_exit(self, *args):
        for topic in self._controller.list():
            self._controller.remove(topic)
        raise ExitCmdException()

    def do_set_user(self, user: str):
        """Command to configure user

        Args:
            user (str): Username
        """
        self.do_enter_topic(user)
        self._user = user
