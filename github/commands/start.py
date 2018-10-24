from config import URL
from .base import CommandBase
from classes.chat_controller import ChatController


class CommandStart(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        self.set_bot(payload)

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)

        link = "{}/github/{}".format(URL, chat["user"])

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
