import os
import feedparser
import datetime
import time
import requests
import json
import argparse
import random
import yaml
from tpns_functions import push_post
import re
import hashlib
import base64
from dateutil import parser

# folder structure:
# Notification/
#   main.py
#   tpns_functions.py
#   cache/
#     sent_url_hash
#     xml/
#       example.xml


def create_hash(string: str) -> str:
    return base64.b64encode(hashlib.sha256(string.encode('utf-8')).digest())


def check_post(post: json) -> bool:
    post_hash = create_hash(post.title + post.link)

    if os.path.exists(f"cache/{post_hash}"):
        return False

    else:
        # check if within 1 day
        post_update_time = parser.parse(post.published)
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - post_update_time < datetime.timedelta(days=1)


def post_time(post: json) -> str:
    post_update_time = parser.parse(post.published).astimezone(
        datetime.timezone(datetime.timedelta(hours=8)))

    return post_update_time.strftime("%Y-%m-%d %H:%M:%S")


def main():
    for xml_file in os.listdir("cache/xml"):
        feed = feedparser.parse(f"cache/xml/{xml_file}")

        for post in feed.entries:
            if check_post(post):
                try:
                    response = ""
                    response += push_post(post, dev_channel=True,
                                          time=post_time(post))
                    time.sleep(1)
                    response += "\n"
                    response += push_post(post, dev_channel=False,
                                          time=post_time(post))
                    time.sleep(1)

                    post_hash = create_hash(post.title + post.link)
                    with open(f"cache/{post_hash}", "w") as f:
                        f.write(response)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    main()
