from data_types.commit import Commit
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventPush(EventBase):

    repository = None
    sender = None
    commits = []

    """
    PushEvent

    Triggered when a repository branch is pushed to.
    In addition to branch pushes, webhook push events are also triggered when repository tags are pushed.

    https://developer.github.com/v3/activity/events/types/#pushevent
    """

    async def process(self, payload, chat_id):
        """
        Processes Push event
        :param payload: JSON object with payload
            ref             string      The full Git ref that was pushed. Example: "refs/heads/master".
            head            string      The SHA of the most recent commit on ref after the push.
            before          string      The SHA of the most recent commit on ref before the push.
            size            integer     The number of commits in the push.
            distinct_size   integer     The number of distinct commits in the push.
            commits         array       An array of commit objects describing the pushed commits.
                                        (The array includes a maximum of 20 commits.
                                        If necessary, you can use the Commits API to fetch additional commits.
                                        This limit is applied to timeline events only
                                        and isn't applied to webhook deliveries.)

            compare Compare URL in repository

            pusher  Data of pusher user. Contains 'name' and 'email' fields
            sender  Who sends event
        :param chat_id: current user chat token
        :return:
        """

        self.sdk.log("Ping event payload taken {}".format(payload))

        try:

            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

            for commit in payload['commits']:
                self.commits.append(Commit(commit))

        except Exception as e:
            self.sdk.log('Cannot process PingEvent payload because of {}'.format(e))

        # Start building message

        message = '{} pushed {} {} to {} \n\n'.format(
            self.sender.login,
            len(self.commits),
            "commits" if len(self.commits) > 1 else "commit",
            payload['ref']
        )

        # Compose lists of added|removed|modified filenames

        added = []
        removed = []
        modified = []

        for commit in self.commits:

            # Append commits messages
            message += '* {}\n'.format(commit.message)

            if len(commit.added):
                added.extend(commit.added)
            if len(commit.removed):
                removed.extend(commit.removed)
            if len(commit.modified):
                modified.extend(commit.modified)

        if len(added):
            message += '\nNew files: \n'
            for file_name in added:
                message += file_name + '\n'

        if len(removed):
            message += '\nRemoved files: \n'
            for file_name in removed:
                message += file_name + '\n'

        if len(modified):
            message += '\nModified files: \n'
            for file_name in modified:
                message += file_name + '\n'

        message += '\n ' + payload['compare']

        await self.send(
            chat_id,
            message
        )