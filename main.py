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
    
def checkConfig(name: str):
    if not name in config:
        print(f"config.yaml is invalid! No {name} found!")
        sys.exit(1)
        
for name in ["feeds", "backupDir", "hostingURL"]:
    checkConfig(name)

# create backupDir if it doesn't exist
# backupDir is relative path to main.py
backupDir = config["backupDir"]
if not os.path.exists(backupDir):
    os.makedirs(backupDir)

# backup all feeds
for feedURL in config["feeds"]:
    RSSBackup.backupRSSFeed(feedURL, backupDir, config["hostingURL"])