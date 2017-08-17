# GitHub plugin for CodeX Bot platform

Improve your working process with clever GitHub integration

## Features
Getting notifications about:
- Opening/closing `Pull Requests`
- Creating issues
- Assigning to issues
- Approving or requesting changes on `Pull Requests`

## Getting started

Add [@codex_bot](https://t.me/codex_bot) to chat.

Press button start

Type /apps to see a list of available applications

Choose /github command. It will help you to organize notifications about your git repository activities

## Setting up a repository

Type in command /github_start and and follow further instructions.

1) Choose a repository you want to get notifications from. Open its settings

![alt text](https://user-images.githubusercontent.com/15448200/29360021-ae0cfef6-8289-11e7-8f46-df8595d786fc.png "Open repository settings")

2) Go to "Webhooks" and press button "Add webhook"

![alt text](https://user-images.githubusercontent.com/15448200/29361295-a00fd890-828f-11e7-8d1b-19724334ac6f.jpg "Go to Webhooks section")

3) Copy the link, which bot gives you, into the "Payload URL" field.

You'll get something similar to this
```
https://github.bot.ifmo.su/github/ABCD1234

```
4) For «Content type» choose «application/json».

5) For «Which events would you like to trigger this webhook?» choose
«Send me everything.»

6) Press button «Add webhook».

7) If everything is ok, you'll get message

👏 Repository <b>repository_name</b> successfully linked. Boom.

8) Enjoy 😉

## See it works

Now commit something to your repository, open a `Pull Request`, etc. Get message into chat

## CodeX Team

https://ifmo.su

team@ifmo.su
