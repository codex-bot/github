import random
import string
from time import time

from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER


class Notify:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Notify module initialized")

        self.sdk.register_commands([
            ('notify_help', 'help', self.help),
            ('notify_start', 'start', self.start)
        ])

        self.sdk.set_routes([
            ('POST', '/notify/{user_token}', self.notify_route_handler)
        ])

        self.sdk.start_server()

    #
    #
    # HELP
    # todo: move to the class
    #

    async def help(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))
        await self.sdk.send_to_chat(
            payload["chat"],
            "Это приложение позволяет отправлять разные уведомления в чат с помощью простых запросов. "
            "И его очень просто интегрировать. \n\n "
            "/notify_start — получить ссылку для передачи сообщений в этот чат"
        )

    #
    #
    # START
    # todo: move to the class
    #

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    """
    We will store user-to-chat linking in this collection
    _id | chat | user | dt_register
    """
    CHATS_COLLECTION_NAME = 'chats'

    async def start(self, payload):

        registered_chat = self.sdk.db.find_one(self.CHATS_COLLECTION_NAME, {'chat': payload['chat']})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': payload['chat'],
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(self.CHATS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        message = "Адрес для отправки уведомлений в этот чат: {}/notify/{}\n\n" + \
                  "Сообщение отправляйте в POST-параметре «message»"

        await self.sdk.send_to_chat(
            payload["chat"],
            message.format(URL, user_token)
        )

    #
    #
    # Route /notify/{user_token} handler
    #
    #
    @CodexBot.http_response
    async def notify_route_handler(self, request):
        """
        :param request: - request data:
            - text
            - post
            - json
            - params - should contain {user_token}
        :return:
        """
        self.sdk.log('Notification accepted {}'.format(request['text']))

        # Check for route-token passed
        if 'user_token' not in request['params']:
            self.sdk.log("Notify route handler: user_token is missed")
            return {
                'status': 404
            }

        # Check for post parameter 'message'
        if 'message' not in request['post'] :
            self.sdk.log("Notify route handler: param 'message' missed")
            return {
                'text': "Error: param «message» is missed"
            }

        message = request['post']['message']
        user_token = request['params']['user_token']

        # Get user data from DB by user token
        registered_chat = self.sdk.db.find_one(self.CHATS_COLLECTION_NAME, {'user': user_token})

        # Check if chat was registered
        if not registered_chat or 'chat' not in registered_chat:
            self.sdk.log("Notify route handler: wrong user token passed")
            return {
                'status': 404
            }

        # Send notification
        await self.sdk.send_to_chat(registered_chat['chat'], message)

        # Response
        return {
            'text': 'OK!'
        }


if __name__ == "__main__":
    notify = Notify()
