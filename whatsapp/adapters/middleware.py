"""Defines middleware for pubsub"""
import binascii
import os
import zmq


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
        self.ctx = zmq.Context.instance()
        self._input_port = input_port
        self._publisher_external_port = publisher_external_port

        # Server (publisher sees)
        self.server = self.ctx.socket(zmq.SUB)
        self.server.bind(f"tcp://*:{self._input_port}")
        self.server.setsockopt(zmq.SUBSCRIBE, b"")

        # External Publisher (consumer sees)
        self.publisher = self.ctx.socket(zmq.PUB)
        self.publisher.bind(f"tcp://*:{self._publisher_external_port}")

    def start(self):
        """Starts the server and the internal services
        """
        try:
            zmq.device(zmq.FORWARDER, self.server, self.publisher)  # pylint: disable=no-member
        except Exception as _:
            self.stop()

    def stop(self):
        """Gracefully closes the server
        """
        self.server.close()
        self.publisher.close()
        self.ctx.term()
