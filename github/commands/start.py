import random
import string
from time import time

from config import URL, USERS_COLLECTION_NAME
from .base import CommandBase

class CommandStart(CommandBase):

    @staticmethod
    def generate_user_token():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    async def __call__(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        self.set_bot(payload)

        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'chat': payload['chat']})

        if registered_chat:
            user_token = registered_chat['user']
        else:
            user_token = self.generate_user_token()
            new_chat = {
                'chat': payload['chat'],
                'user': user_token,
                'dt_register': time()
            }
            self.sdk.db.insert(USERS_COLLECTION_NAME, new_chat)
            self.sdk.log("New user registered with token {}".format(user_token))

        link = "{}/github/{}".format(URL, user_token)

        await self.send(
            payload["chat"],
            "To connect repository notifications follow next steps:"
        )

        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo='{}/img/step_1.jpg'.format(URL),
            caption="1) Open repository settings.",
            bot=self.bot
        )

        await self.sdk.send_image_to_chat(
            payload['chat'],
            photo='{}/img/step_2.jpg'.format(URL),
            caption="2) Go to \"Webhooks\" and press button \"Add webhook\".",
            bot=self.bot
        )

        message = "3) Paste in the \"Payload URL\" field this link.\n{}\n" \
                  "\n" \
                  "4) For «Content type» choose «application/json».\n" \
                  "\n" \
                  "5) For «Which events would you like to trigger this webhook?» choose \n" \
                  "«Send me everything.»\n" \
                  "\n" \
                  "6) Press button «Add webhook».".format(link)

        await self.send(
            payload["chat"],
            message
        )
