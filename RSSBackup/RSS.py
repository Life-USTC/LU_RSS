"""
Backup given RSS feed url to a file.
This also includes downloading everything from the feed and saving them locally, like css, images, etc.
"""
import feedparser
import os
import urllib
import hashlib
import re
import json
from typing import Optional

url_matcher = re.compile(
    r'(?<=["])(?:http|https):\/\/[a-zA-Z0-9\?&%-=_\.\/]*(?=["])')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
}

def repeat_download(url, retry_count= 0, max_retry=3):
    """
    Repeat downloading the xml until it succeeds

    :param str url: The url to download
    :param int retry_count: The current retry count
    :param int max_retry: The maximum retry count

    :return: The downloaded data
    :raises Exception: If the retry count is greater than the maximum retry count
    """
    if retry_count > max_retry:
        raise Exception("Cannot download xml file")
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as f:
            data = f.read()
        return data
    except Exception as e:
        print("Error: " + str(e))
        print("Retrying...")
        return repeat_download(url, retry_count + 1, max_retry)

def download_and_convert_url(original_xml: str, url: str, hosting_url: Optional[str], static_dir: str):
    """
    Download the given url and convert it to a local url

    :param str original_xml: The original xml string
    :param str url: The url to convert
    :param str hosting_url: The URL of the website that hosts the feed, if not given, no links will be changed
    :param str static_dir: The directory to save the downloaded files

    :return: The converted xml string
    :raises: None
    """
    try:
        filename = hashlib.sha256(url.encode("utf-8")).hexdigest()
        filenamePath = os.path.join(static_dir, filename)

        if os.path.exists(filenamePath):
            print("File " + filenamePath + " exists, skipping...")
        else:
            print("Downloading " + url + " to " + filenamePath)
            data = repeat_download(url)
            with open(filenamePath, "wb") as f:
                f.write(data)

        # Convert url
        if hosting_url is not None:
            original_xml = original_xml.replace(
                url, hosting_url + "/static/" + filename)
        return original_xml
    except Exception as e:
        print("Error: " + str(e))
        return original_xml


def backupRSSFeed(feedURL: str, output_dir: str, hosting_URL: str, xml_filename: Optional[str] = None):
    """
    Backup given RSS feed url and its contents to a folder

    :param str feedURL: The URL of the RSS feed
    :param str outputDir: The directory to output the results
    :param str hostingURL: The URL of the website that hosts the feed, if not given, no links will be changed
    :param str xmlFilename: The filename of the xml file, if not given, the feed name will be used

    :return: None
    :raises: None

    :description:
        * outputDir folder structure
            ```txt
            outputDir/
                static/
                    example_image.png
                xml/
                    feed_name.xml (or xmlFilename.xml if xmlFilename is not None)
                feed_list.json
        ```
        * Notice on static folder
            No file get deleted, only added
            Files are named: sha256(url), file extension is ignored
        * Notice on xml folder
            If feed_name.xml already exists, it won't be simply overwritten
            but instead, the new entries will be added to the front of the file
            !! TODO: Increasement on RSS xml is bit difficult,
            !! the current behaviour is overwritten than merged
    """

    print("Backing up " + feedURL)
    staticDir = os.path.join(output_dir, "static")
    xmlDir = os.path.join(output_dir, "xml")
    for dir in [output_dir, staticDir, xmlDir]:
        if not os.path.exists(dir):
            os.makedirs(dir)

    print("Downloading xml file...")
    original_xml = repeat_download(feedURL).decode("utf-8")
    feedName = feedparser.parse(original_xml).feed.title
    if feedName == "":
        feedName = hashlib.sha256(feedURL.encode("utf-8")).hexdigest()
    feedXMLFilename = feedName + ".xml" if xml_filename is None else xml_filename
    feedPath = os.path.join(xmlDir, feedXMLFilename)

    print("Downloaded xml file, replacing urls...")
    for url in url_matcher.findall(original_xml):
        original_xml = download_and_convert_url(original_xml, url, hosting_URL, staticDir)

    print("Replacing urls done, saving xml file...")
    if os.path.exists(feedPath):
        os.remove(feedPath)
    with open(feedPath, "w") as f:
        f.write(original_xml)
    print("Backup of " + feedName + " is done.")
