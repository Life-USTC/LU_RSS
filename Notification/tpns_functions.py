"""
tpns_functions.py

This file contains the function to push a feed to TPNS.
"""
import datetime
import os
from tpns import Push
from tpns.core.authenticators import BasicAuthenticator
import json
import time
import html2text

tpns_user_name = os.environ["TPNS_USER_NAME"]
tpns_secret_key = os.environ["TPNS_SECRET_KEY"]

if "DEBUG" in os.environ:
    debug_symb = bool(os.environ["DEBUG"])
else:
    debug_symb = False

authenticator = BasicAuthenticator(username=tpns_user_name,
                                   password=tpns_secret_key)
ios_push = Push(authenticator=authenticator, zone="sh")

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.ignore_tables = True
h.ignore_anchors = True
h.unicode_snob = True


def push_post(post: json, dev_channel: bool, time: str):
    if debug_symb:
        print("Pushing to TPNS:")
        print(post.title)
        print(post.link)
        return

    title = post["title"].replace("\n", "").replace("\r", "")[:25]
    description = h.handle(post["description"]).replace("\n", "").replace("\r", "")[:50]

    push_data = {
        "audience_type": "all",
        "environment": "product",
        "message_type": "notify",
        "message": {
            "title": title,
            "content": description,
            "ios": {
                "aps": {
                    "alert": {
                        "subtitle": "",
                    },
                    "badge_type": -2,
                },
                "custom_content": '{"key":"value"}',
                "xg": "oops",
            },
        },
    }
    if "author" in post:
        push_data["message"]["ios"]["aps"]["alert"]["subtitle"] = post.author

    if dev_channel:
        push_data["environment"] = "dev"
        push_data["message"]["ios"]["aps"]["alert"]["subtitle"] += "  [" + time + "]"

    response = ios_push.push(
        audience_type=push_data["audience_type"],
        message=push_data["message"],
        message_type=push_data["message_type"],
        environment=push_data["environment"],
    )

    print(json.dumps(response.get_result(), indent=2))
    return json.dumps(response.get_result(), indent=2)
