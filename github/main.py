import requests

from github.sdk.codexbot_sdk import CodexBot
from github.sdk.components.server import http_response


class GitHub:
    __name__ = "GitHub"

    routes = []

    sdk = None

    core_host = "http://127.0.0.1:1337/handshake"

    def __init__(self):
        delegated_queue_name = self.handshake()
        self.sdk = CodexBot(delegated_queue_name)

        self.sdk.set_routes([
            ('GET', '/test', self.test_route_handler)
        ])

        self.sdk.log("GitHub module inited")
        self.sdk.start_server()

    def handshake(self):
        """
        Requests queue name from core broker
        :return:
        """
        response = requests.post(self.core_host, data={'tool': self.__name__})

        queue_name_received = None

        if response.ok and response.status_code == 200:
            print('Handshake given {}'.format(response.text))
            queue_name_received = response.text
        else:
            Exception("Handshake failed")

        return queue_name_received


    @http_response
    def test_route_handler(self, text, post, json):
        """
        Process messages from telegram bot
        :return:
        """
        self.sdk.log("Got test route callback {} {} {}".format(text, post, json))

        return True


github = GitHub()

