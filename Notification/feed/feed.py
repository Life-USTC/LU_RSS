"""
- feed.py

- This file is used to model the feed.
- Main features include:
    - parse feed from given url
    - model feed
    - determine who to push to (with labels, using LLMs to determine which label to push to)
    - database operations to store feed

@author: TiankaiMa
@version: 0.1
@date: 2023.06.07
@last_modified: 2023.06.07
"""
import feedparser
import sqlite3
import os
import time
import datetime
import pytz
import re
import json
import requests
from typing import *


class Feed:
    def __init__(self,
                 title: str,
                 link: str,
                 description: str,
                 pubdate: str,
                 source: str,
                 id: Optional[int] = None):
        self.title = title
        self.link = link
        self.description = description
        self.pubdate = pubdate
        self.source = source
        # if self.id is None, set it from hashcode of link
        if id is None:
            self.id = hash(link)
        else:
            self.id = id

        self.labels = []  # don't parse labels here to make __init__ instant

    def get_labels(self):
        """
        get labels from title and description
        """
        # LLMs are used to determine which label to push to
        # certain hints are given to the API, as well as the title, description perhaps the content inside the link


class FeedSource:
    def __init__(self, url: str, timezone: str, id: Optional[int] = None):
        self.url = url
        self.timezone = timezone
        # if self.id is None, set it from hashcode of url
        if id is None:
            self.id = hash(url)
        else:
            self.id = id

        self.raw_feed = ""  # don't parse the feed here to make __init__ instant

    def get_raw_feed(self):
        """
        get raw feed from url
        """
        self.raw_feed = feedparser.parse(self.url)

    def parse_feed(self) -> list[Feed]:
        pass
