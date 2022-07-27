"""Defines middleware for pubsub"""
import binascii
import os
from random import randint
from threading import Thread
import time

from zmq.devices import monitored_queue
import zmq


def listener_thread(pipe):
    """Thread to debug internal messages
    """
    while True:
        try:
            print('LISTENER', pipe.recv_multipart())
        except zmq.ZMQError as exc:
            if exc.errno == zmq.ETERM:
                break           # Interrupted


def zpipe(ctx):
    """build inproc pipe for talking to threads
    mimic pipe used in czmq zthread_fork.
    Returns a pair of PAIRs connected via inproc
    """
    socket_a = ctx.socket(zmq.PAIR)
    socket_b = ctx.socket(zmq.PAIR)
    socket_a.linger = socket_b.linger = 0
    socket_a.hwm = socket_b.hwm = 1
    iface = f"inproc://{binascii.hexlify(os.urandom(8))}"
    socket_a.bind(iface)
    socket_b.connect(iface)
    return socket_a, socket_b


class PubSubProxy:
    """Proxy pubsub
    """

    def __init__(
        self,
        input_port: int,
        publisher_external_port: int
    ):
        """
        Args:
            input_port (int): Port to receive messages
            publisher_external_port (int): Port to send messages
        """
        ctx = zmq.Context.instance()
        self.pipe = zpipe(ctx)
        self._input_port = input_port
        self._publisher_external_port = publisher_external_port

        # Server (publisher sees)
        self.server = ctx.socket(zmq.REP)
        self.server.bind(f"tcp://*:{self._input_port}")

        # Internal Publisher (internal subscriber and server sees)
        self.publisher = ctx.socket(zmq.PUB)
        self.publisher.bind(f"tcp://*:{randint(6500, 7000)}")

        # Internal Subscriber
        self.subscriber = ctx.socket(zmq.XSUB)
        self.subscriber.connect(f"tcp://localhost:{randint(6500, 7000)}")

        # External Publisher (consumer sees)
        self.publisher = ctx.socket(zmq.XPUB)
        self.publisher.bind(f"tcp://*:{self._publisher_external_port}")

    def _serve(self):
        """Serves the Pub/Sub implementation
        """
        while True:
            #  Wait for next request from client
            message = self.server.recv()
            time.sleep(.01)
            self.server.send("received".encode('utf-8'))
            self.publisher.send(message)

    def start(self):
        """Starts the server and the internal services
        """
        l_thread = Thread(target=listener_thread, args=(self.pipe[1],))
        l_thread.start()
        server_thread = Thread(target=self._serve, args=())
        server_thread.start()
        monitored_queue(
            self.subscriber,
            self.publisher,
            self.pipe[0],
            b'pub',
            b'sub'
        )
