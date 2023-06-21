import yaml
import os
import sys
import RSSBackup
import RSSGenerate
import feedparser
import json


def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    for name in ["backup_feeds", "outputDir", "hostingURL"]:
        if not name in config:
            print(f"config.yaml is invalid! No {name} found!")
            sys.exit(1)

    return config


def backup_feeds(config):
    output_dir = config["outputDir"]
    hosting_URL = config["hostingURL"]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Backup all feeds
    for feed in config["backup_feeds"]:
        if isinstance(feed, str):
            RSSBackup.backupRSSFeed(feedURL=feed,
                                    output_dir=output_dir,
                                    hosting_URL=hosting_URL)
        elif isinstance(feed, dict):
            RSSBackup.backupRSSFeed(feedURL=feed["url"],
                                    output_dir=output_dir,
                                    hosting_URL=hosting_URL,
                                    xml_filename=feed["xmlFilename"])
        else:
            print("Invalid feed: " + str(feed))
            sys.exit(1)


def generate_feeds(config):
    output_dir = config["outputDir"]
    RSSGenerate.generate_RSS_feeds(output_dir=output_dir)


def make_index(config):
    """
    Make README.md, with every feed's name and link (everything inside outputDir/xml/)

    :param dict config: The config dict

    :return: None
    """
    output_dir = config["outputDir"]

    # list all xml files
    xml_dir = os.path.join(output_dir, "xml")
    xml_files = os.listdir(xml_dir)
    xml_files = [os.path.join(xml_dir, f) for f in xml_files]
    xml_files = [f for f in xml_files if os.path.isfile(f)]

    # make index
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write("# RSS Feeds\n\n[![Create feeds](https://github.com/Life-USTC/LU_RSS/actions/workflows/run.yaml/badge.svg)](https://github.com/Life-USTC/LU_RSS/actions/workflows/run.yaml)\n\n")
        for xml_file in xml_files:
            xml_file_name = xml_file.split("/")[-1]
            with open(xml_file, "r") as f2:
                feed = feedparser.parse(f2.read())
            title = feed.feed.title if len(
                feed.feed.title) > 0 else xml_file_name
            relative_xml_file = xml_file.replace(output_dir, "")
            f.write(f"""
* {title}:
> [{xml_file_name}]({relative_xml_file})
>
> Deployed at: {config['hostingURL']}{relative_xml_file}
""")


def make_old_index_json(config):
    """
    Make feed_list.json, format like this:

    ```json
    [{
        "name": "\u516c\u4f17\u53f7\u300c\u4e2d\u56fd\u79d1\u5b66\u6280\u672f\u5927\u5b66\u300d",
        "url": "https://cdn.werss.weapp.design/api/v1/feeds/fd85a6cc-1073-4d7f-872b-d662c08761cd.xml",
        "xml": "./backup/xml/mp_ustc_main.xml",
        "backupURL": "https://rss-cdn.tiankaima.dev/xml/mp_ustc_main.xml"
    }]
    ```

    :param dict config: The config dict

    :return: None
    """
    output_dir = config["outputDir"]

    # list all xml files
    xml_dir = os.path.join(output_dir, "xml")
    xml_files = os.listdir(xml_dir)
    xml_files = [os.path.join(xml_dir, f) for f in xml_files]
    xml_files = [f for f in xml_files if os.path.isfile(f)]

    # make index
    feed_list = []
    for xml_file in xml_files:
        xml_file_name = xml_file.split("/")[-1]
        with open(xml_file, "r") as f:
            feed = feedparser.parse(f.read())
        title = feed.feed.title if len(feed.feed.title) > 0 else xml_file_name
        feed_list.append({
            "name": title,
            "url": "deprecated",
            "xml": xml_file,
            "backupURL": config["hostingURL"] + "/backup/xml/" + xml_file_name
        })

    with open(os.path.join(output_dir, "feed_list.json"), "w") as f:
        f.write(json.dumps(feed_list, indent=4))


def make_new_index_json(config):
    pass


def main():
    config = load_config()
    backup_feeds(config)
    generate_feeds(config)
    make_index(config)
    make_old_index_json(config)


if __name__ == "__main__":
    main()
