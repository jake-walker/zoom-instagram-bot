# Zoom Instagram Bot

A small program to check an Instagram chat for Zoom links and send them to Discord via a webhook.

> *This was designed to get working quickly so it isn't the nicest code in the world! It works well enough for the time being and I might end up putting more time into making it better in the future.*

## Usage

Firstly, install the programs dependencies using [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

```
pipenv install
```

Next, set the username and password environment variables

```
export BOT_USERNAME="myusername"
export BOT_PASSWORD="mypassword"
```

Then, run the bot for the first time. It will detect that it has not been told a thread to check and it will show the available threads and quit.

```
python bot.py
[I 200413 12:10:26 bot:53] Logged in as test
[{"id": "1234", "name": "test1"}, {"id": "5678", "name": "test2"}, {"id": "123345", "name": "test3"}, {"id": "1245663", "name": "test4"}, {"id": "64567423", "name": "test5"}]
```

Then using that output, find the chat that you want to check and copy the ID. If the chat is not in the list, you might need to send a message to the chat and try again. Also, get a Discord webhook URL. Now using the collected thread ID and Discord webhook URL, set the environment variables

```
export BOT_THREAD_ID="1234"
export BOT_WEBHOOK_URL="https://discordapp.com/api/webhooks/1234/5678"
```

Finally, start the bot again:

```
python bot.py
[I 200413 13:13:47 bot:53] Logged in as test
[D 200413 13:13:47 bot:61] Getting messages!
```

## Known Issues

- Links are sent multiple times to Discord.
- All `vh7.uk` URLs are also sent even if they are not Zoom links.

## New Feature List

This is a small list of cool features that would be cool to build into this program in the future.

- Shorten links before they are sent to Discord.
- Shorten links and send them back to Instagram.
- Detect shortened links sent on Instagram.
