"""
This file reads from config.yaml and starts the program.
"""
import yaml
import os
import sys
import RSSBackup

# load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


for name in ["feeds", "backupDir", "hostingURL"]:
    if not name in config:
        print(f"config.yaml is invalid! No {name} found!")
        sys.exit(1)

# create backupDir if it doesn't exist
# backupDir is relative path to main.py
backupDir = config["backupDir"]
if not os.path.exists(backupDir):
    os.makedirs(backupDir)

# backup all feeds
for feed in config["feeds"]:
    # here, feed could either be a string or a dict
    if isinstance(feed, str):
        RSSBackup.backupRSSFeed(feedURL=feed,
                            backupDir=backupDir,
                            hostingURL=config["hostingURL"])
    elif isinstance(feed, dict):
        RSSBackup.backupRSSFeed(feedURL=feed["url"],
                            backupDir=backupDir,
                            hostingURL=config["hostingURL"],
                            xmlFilename=feed["xmlFilename"])
    else:
        print("Invalid feed: " + str(feed))
        sys.exit(1)
