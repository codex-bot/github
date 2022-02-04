import json
import logging

from commands.branch import CommandBranch
from events.fork import EventFork
from events.repository import EventRepository
from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER, HAWK_CATCHER_SETTINGS
from config import USERS_COLLECTION_NAME
from commands.help import CommandHelp
from commands.start import CommandStart
from commands.link import CommandLink
from commands.verbose import CommandVerbose
from events.ping import EventPing
from events.push import EventPush
from events.issues import EventIssues
from events.discussions import EventDiscussions
from events.issue_comment import EventIssueComment
from events.pull_request import EventPullRequest
from events.pull_request_review import EventPullRequestReview
from events.watch import EventWatch
from hawkcatcher import Hawk


class Github:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN, hawk_params=HAWK_CATCHER_SETTINGS)

        self.sdk.log("Github module initialized")

        self.sdk.register_commands([
            ('github',
             'GitHub app. Allows you receive notices about new issues, commits and pull-requests.',
             CommandHelp(self.sdk)),
            ('github_help', 'help', CommandHelp(self.sdk)),
            ('github_start', 'start', CommandStart(self.sdk)),
            ('github_link', 'link', CommandLink(self.sdk)),
            ('github_branch', 'branch', CommandBranch(self.sdk)),
            ('github_verbose', 'verbose', CommandVerbose(self.sdk)),
        ])

        self.sdk.set_routes([
            ('POST', '/github/{user_token}', self.github_callback_handler)
        ])

        self.sdk.set_path_to_static('/img', 'static/img')

        self.sdk.start_server()

    @CodexBot.http_response
    async def github_callback_handler(self, request):

        # Check for route-token passed
        if 'user_token' not in request['params']:
            self.sdk.log("GitHub route handler: user_token is missed")
            return {
                'status': 404
            }

        # Get user data from DB by user token passed in URL
        user_token = request['params']['user_token']
        registered_chat = self.sdk.db.find_one(USERS_COLLECTION_NAME, {'user': user_token})

        # Check if chat was registered
        if not registered_chat or 'chat' not in registered_chat:
            self.sdk.log("GitHub route handler: wrong user token passed")
            return {
                'status': 404
            }

        event_name = request['headers']['X-Github-Event']

        events = {
            'watch': EventWatch(self.sdk),
            'fork': EventFork(self.sdk),
            'ping': EventPing(self.sdk),
            'push': EventPush(self.sdk),
            'issues': EventIssues(self.sdk),
            'issue_comment': EventIssueComment(self.sdk),
            'pull_request': EventPullRequest(self.sdk),
            'pull_request_review': EventPullRequestReview(self.sdk),
            'repository': EventRepository(self.sdk),
            'discussion': EventDiscussions(self.sdk)
        }

        if event_name not in events:
            self.sdk.log("Github webhook callback: unsupported event taken: {}".format(event_name))
            return {
                'status': 404
            }

        try:
            # GitHub might pass JSON as request body
            payload = json.loads(request['text'])
        except Exception as e:
            self.sdk.log('Payload from GitHub is not JSON: {}'.format(e))
            self.sdk.hawk.catch()

            return {
                'status': 400
            }

        try:
            # Call event handler
            events[event_name].set_bot(registered_chat)
            await events[event_name].process(payload, registered_chat)

            return {
                'text': 'OK',
                'status': 200
            }

        except Exception as e:
            self.sdk.log('Cannot handle request from GitHub: {}'.format(e))
            self.sdk.hawk.catch()

            return {
                'status': 500
            }


if __name__ == "__main__":
    github = Github()
