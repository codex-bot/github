from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        self.set_bot(payload)

        message = "This GitHub app allows you stay in touch with all updates for your repository.\n" \
                  "You won't miss any issue, assignee, pull request or approve."

        # TODO get repos list
        repositories = list()

        if not repositories:
            message += "You have not connected any repository in this chat.\n\n" \
                       "Set up the first right now by /github_start."
        # else:
        #     message += "Подключенные репозитории.\n\n"
        #     for repository in repositories:
        #         message += "{}\n".format(repository["name"])
        #     message += "\nДля отключения репозитория используйте команду /github_stop\n" \
        #            "Подключить еще один репозиторий можно с помощью команды /github_start\n\n" \
        #            "Меню модуля: /github_help"

        await self.send(
            payload["chat"],
            message
        )
