from .base import CommandBase


class CommandHelp(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))

        self.set_bot(payload)

        message = "This GitHub app allows you stay in touch with all updates for your repository. " \
                  "You won't miss any issue, assignee, pull request or approve.\n" \
                  "To work with the github_bot you can use these commands:\n" \
                  "  - To connect new repository use: /github_start\n" \
                  "  - To set verbosity mode use: /github_verbose\n" \
                  "  - To get link to the chat use: /github_link\n" \
                  "  - To receive notifications from a branch use: /github_branch\n" \
                  "  - To get help use: /github_help"

        # TODO get repos list
        # repositories = list()
        #
        # if not repositories:
        #     message += "You have not connected any repository in this chat.\n\n" \
        #                "Set up the first right now by /github_start."
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
