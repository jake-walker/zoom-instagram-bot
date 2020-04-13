from instagram_private_api import Client
import json
import sys
from urllib.parse import urlparse
from discord_webhook import DiscordWebhook
import datetime
import time
from logzero import logger
import os


# Function for getting the latest threads that the bot can access
def get_threads(inbox):
    threads = inbox["inbox"]["threads"]
    # Create an list of thread ids and names
    output = []
    for thread in threads:
        output.append({
            "id": thread["thread_id"],
            "name": thread["thread_title"]
        })
    return output


# Function for getting an instagram thread
def get_thread(api, thread_id, cursor=None):
    endpoint = "direct_v2/threads/{0}".format(thread_id)
    if cursor is not None:
        endpoint += "?cursor={0}".format(cursor)
    return api._call_api(endpoint)["thread"]


# The username and password of the instagram account
username = os.getenv("BOT_USERNAME", None)
password = os.getenv("BOT_PASSWORD", None)
# The thread id to check for messages from
thread_id = os.getenv("BOT_THREAD_ID", None)
# The discord webhook url to send notifications to
webhook_url = os.getenv("BOT_WEBHOOK_URL", None)
# The message template to use ({1} for the number of seconds, {0} for the link)
message_template = os.getenv("BOT_MESSAGE_TEMPLATE", ("**:rotating_light: "
                             "Alert!** A possible Zoom URL has been posted on "
                             "the Instagram group chat ({1} seconds ago): "
                             "{0}"))
# The number of seconds old that the message has to be before it is too 'stale'
# to send
max_link_age = int(os.getenv("BOT_MAX_LINK_AGE", "300"))
# The number of seconds to wait between each check
sleep_time = int(os.getenv("BOT_SLEEP_TIME", "100"))

# Create a new
api = Client(username, password)
logger.info("Logged in as {}".format(api.authenticated_user_name))

if thread_id is None:
    inbox = api.direct_v2_inbox()
    print(json.dumps(get_threads(inbox)))
    sys.exit(0)

while True:
    logger.debug("Getting messages!")
    thread = get_thread(api, thread_id)

    for message in thread["items"]:
        if message["item_type"] != "link":
            continue

        msg_time = datetime.datetime.fromtimestamp(int(
            str(message["timestamp"])[:10]))
        time_diff = datetime.datetime.now() - msg_time
        time_diff_s = time_diff.total_seconds()

        if time_diff_s > max_link_age:
            continue

        url = message["link"]["link_context"]["link_url"]
        url_parsed = urlparse(url)

        if (url_parsed.netloc.endswith("zoom.us") or
                url_parsed.netloc.endswith("vh7.uk")):
            logger.info("FOUND ZOOM LINK -> {}".format(url))
            webhook = DiscordWebhook(url=webhook_url,
                                     content=message_template.format(
                                         url, int(time_diff_s)))
            webhook.execute()
        else:
            logger.debug("FOUND LINK -> {}".format(url))

    time.sleep(sleep_time)
