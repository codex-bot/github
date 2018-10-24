import random
import string
from time import time

from config import USERS_COLLECTION_NAME


class ChatController:

    def __init__(self, sdk):
        self.sdk = sdk

    def get_chat(self, chat_id, bot_id):
        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': chat_id, 'bot': bot_id})

        if registered_chat:
            return registered_chat
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': chat_id,
                'user': user_token,
                'bot': bot_id,
                'dt_register': time(),
                'branch': "*"
            }
            self.sdk.log("New user registered with token {}".format(user_token))
            self.sdk.db.insert(USERS_COLLECTION_NAME, new_chat)
            return new_chat

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))