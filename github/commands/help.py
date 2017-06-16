from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
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

        await self.sdk.send_text_to_chat(
            payload["chat"],
            message
        )
