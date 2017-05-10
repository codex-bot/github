import asyncio

from .components.broker import Broker
from .components.server import Server
from .components.logging import Logging
from .config import SERVER


class CodexBot:

    def __init__(self, delegated_queue_name):
        """
        Initiates SDK
        :param delegated_queue_name: - name of queue that core deligates to this tool
        """

        self.modules = {}

        self.logging = Logging()

        self.event_loop = asyncio.get_event_loop()

        self.broker = self.init_broker(delegated_queue_name)
        self.server = self.init_server()

        self.init_queue()

        self.logging.debug("Initialized")

    def init_queue(self):
        self.logging.debug("Initiate queue and loop.")
        self.broker.start()

    def init_server(self):
        return Server(self.event_loop, SERVER['host'], SERVER['port'])

    def init_broker(self, delegated_queue_name):
        return Broker(self, self.event_loop, delegated_queue_name)

    def log(self, message):
        self.logging.debug(message)

    def start_server(self):
        self.server.start()

    def set_routes(self, routes):
        self.server.set_routes(routes)

