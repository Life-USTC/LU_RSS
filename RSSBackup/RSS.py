"""
Backup given RSS feed url to a file.
This also includes downloading everything from the feed and saving them locally, like css, images, etc.
"""
import feedparser
import os
import urllib
import hashlib
import re

url_matcher = re.compile(r"(https?://[^\s<>\(\)]+)") # avoid matching <> in the url (due to xml)

def backupRSSFeed(feedURL: str, backupDir: str, hostingURL: str):
    """
    Backup given RSS feed url and its contents to a folder
    
    :param feedURL: The URL of the RSS feed
    :param backupDir: The directory to backup the feed to
    :param hostingURL: The URL of the website that hosts the feed, if not given, no links will be changed
    """
    
    # - HOW THE BACKUP FOLDER LOOKS LIKE -
    # backupDir/
    #    static/
    #        example_image.png
    #    xml/
    #       feed_name.xml
    #    feed_list.txt
    # - More Info on static -
    # * No file get deleted, only added
    # * Files are named: sha256(url)
    # - More Info on feed_name.xml -
    # * If feed_name.xml already exists, it won't be simply overwritten
    # * but instead, the new entries will be added to the front of the file
    # !! TODO: Increasement on RSS xml is bit difficult, the current behaviour is overwritten than merged
    
    print("Backing up " + feedURL)
    
    # Create backupDir if it doesn't exist
    if not os.path.exists(backupDir):
        os.makedirs(backupDir)
    
    # Create static folder if it doesn't exist
    staticDir = os.path.join(backupDir, "static")
    if not os.path.exists(staticDir):
        os.makedirs(staticDir)
    
    if not os.path.exists(os.path.join(backupDir, "xml")):
        os.makedirs(os.path.join(backupDir, "xml"))
    
    # Get the feed
    # original_xml = urllib.request.urlopen(feedURL).read().decode("utf-8")
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
    }
    
    req = urllib.request.Request(feedURL, headers=headers)
    with urllib.request.urlopen(req) as response:
        original_xml = response.read().decode("utf-8")
        
    print("Downloaded feed")
    
    feed = feedparser.parse(original_xml)
    feedName = feed.feed.title
    
    # find urls in the feed
    urls = url_matcher.findall(original_xml)
    
    # download all urls
    for url in urls:
        try:
            # get the filename
            filename = hashlib.sha256(url.encode("utf-8")).hexdigest()
            filenamePath = os.path.join(staticDir, filename)
            
            print("Downloading " + url + " to " + filenamePath)
            
            # download the file
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                with open(filenamePath, "wb") as f:
                    f.write(response.read())
            
            # replace the url in the xml
            if hostingURL is not None:
                original_xml = original_xml.replace(url, hostingURL + "/static/" + filename)
        except Exception as e:
            print("Error downloading " + url + ": " + str(e))
    
    # remove feed_name.xml if it exists
    feedPath = os.path.join(backupDir, "xml", feedName + ".xml")
    if os.path.exists(feedPath):
        os.remove(feedPath)
        
    # write the xml to the file
    with open(feedPath, "w") as f:
        f.write(original_xml)
        
    # add the feed to feed_list.txt
    with open(os.path.join(backupDir, "feed_list.txt"), "a") as f:
        f.write(feedName + "\n")
        
    # print the result
    print("Backup of " + feedName + " is done.")
