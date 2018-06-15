import random
import string
from time import time

from applications.metrika.metrika.config import USERS_COLLECTION_NAME


class ChatController:

    def __init__(self, sdk):
        self.sdk = sdk

    def register_chat(self, chat_id):
        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': chat_id})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': chat_id,
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(USERS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        return user_token

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))