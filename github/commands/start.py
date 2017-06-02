from .base import CommandBase


class CommandStart(CommandBase):

    async def start(self, payload):
        self.sdk.log("/start handler fired with payload {}".format(payload))

        message = "Чтобы подключить репозиторий, выполните следующие шаги.\n\n" \
                  "1) Откройте настройки вашего репозитория.\n\n" \
                  "2) Зайдите в раздел Webhooks & services и нажмите кнопку Add Webhook.\n\n" \
                  "3) Вставьте в поле Payload URL следующую ссылку.\n{link}\n\n" \
                  "4) В поле «Which events would you like to trigger this webhook?» выберите " \
                  "«Let me select individual events» и отметьте следующие флажки: \n" \
                  "- Issues\n- Pull request\n- Push\n\n" \
                  "5) В поле «Content type» выберите тип «application/json».\n\n" \
                  "6) Нажмите на кнопку «Add Webhook»."
        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )
