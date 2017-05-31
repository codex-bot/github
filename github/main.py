import random
import string
from time import time

from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER


class Github:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Github module initialized")

        self.sdk.register_commands([
            ('github_help', 'help', self.help),
            ('github_start', 'start', self.start)
        ])

        self.sdk.set_routes([
            # ('POST', '/github/{user_token}', self.github_route_handler)
        ])

        self.sdk.start_server()

    #
    #
    # HELP
    # todo: move to the class
    #

    async def help(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        message = "Модуль для работы с сервисом GitHub.\n\n" \
                  "- Оповещения о новых Push-событиях\n" \
                  "- Оповещения о создании Pull-реквестов\n" \
                  "- Оповещения о создании Issues\n\n" \

        # TODO get repos list
        repositories = list()

        if not repositories:
            message += "В данный момент модуль не активирован.\n\n" \
                       "Для настройки модуля, используйте команду /github_start"
        # else:
        #     message += "Подключенные репозитории.\n\n"
        #     for repository in repositories:
        #         message += "{}\n".format(repository["name"])
        #     message += "\nДля отключения репозитория используйте команду /github_stop\n" \
        #            "Подключить еще один репозиторий можно с помощью команды /github_start\n\n" \
        #            "Меню модуля: /github_help"

        await self.sdk.send_to_chat(
            payload["chat"],
            message
        )

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

if __name__ == "__main__":
    github = Github()
