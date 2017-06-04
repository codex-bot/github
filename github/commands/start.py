import random
import string
from time import time

from github.config import URL
from .base import CommandBase

class CommandStart(CommandBase):

    """
    We will store user-to-chat linking in this collection
    _id | chat | user | dt_register
    """
    USERS_COLLECTION_NAME = 'users'

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))


    async def start(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        registered_chat = self.sdk.db.find_one(self.USERS_COLLECTION_NAME, {'chat': payload['chat']})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': payload['chat'],
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(self.USERS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        link = "{}/github/{}".format(URL, user_token)

        await self.sdk.send_to_chat(
            payload["chat"],
            "Чтобы подключить репозиторий, выполните следующие шаги."
        )

        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo='{}/img/step_1.jpg'.format(URL),
            caption="1) Откройте настройки вашего репозитория."
        )

        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo='{}/img/step_2.jpg'.format(URL),
            caption="2) Зайдите в раздел Webhooks & services и нажмите кнопку Add Webhook."
        )

        message = "3) Вставьте в поле Payload URL следующую ссылку.\n{}\n" \
                  "\n" \
                  "4) В поле «Which events would you like to trigger this webhook?» выберите " \
                  "«Let me select individual events» и отметьте следующие флажки: \n" \
                  "- Issues \n" \
                  "- Pull request \n" \
                  "- Push \n" \
                  "\n" \
                  "5) В поле «Content type» выберите тип «application/json».\n" \
                  "\n" \
                  "6) Нажмите на кнопку «Add Webhook».".format(link)

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

