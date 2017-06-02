from .base import CommandBase
from github.config import URL

class CommandStart(CommandBase):

    async def start(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

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

        message = "3) Вставьте в поле Payload URL следующую ссылку.\n{link}\n\n" \
                  "4) В поле «Which events would you like to trigger this webhook?» выберите " \
                  "«Let me select individual events» и отметьте следующие флажки: \n" \
                  "- Issues\n- Pull request\n- Push\n\n" \
                  "5) В поле «Content type» выберите тип «application/json».\n\n" \
                  "6) Нажмите на кнопку «Add Webhook»."

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

