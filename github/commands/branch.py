from classes.chat_controller import ChatController
from settings import URL, USERS_COLLECTION_NAME
from .base import CommandBase


class CommandBranch(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/github_branch handler fired with payload {}".format(payload))

        self.set_bot(payload)

        branch = payload.get("params", "")
        if not len(branch):
            return await self.send(
                payload["chat"],
                "Please, specify the branch in param:\nExample: /github_branch beta\nUse * for all branches"
            )

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)
        chat["branch"] = branch
        self.sdk.db.update(USERS_COLLECTION_NAME, {'chat': chat['chat'], 'bot': self.bot}, chat)

        await self.send(
            payload["chat"],
            "You will be notified about commits in {} branch".format(branch)
        )
