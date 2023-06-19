import yaml
import os
import sys
import RSSBackup
import RSSGenerate

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
        f.write("# RSS Feeds\n\n")
        for xml_file in xml_files:
            title = xml_file.split("/")[-1]
            relative_xml_file = xml_file.replace(output_dir, "")
            f.write(f"* [{title}]({relative_xml_file})")

            # add CDN link
            f.write(f" -> {config['hostingURL']}{relative_xml_file}\n\n")

def main():
    config = load_config()
    backup_feeds(config)
    generate_feeds(config)
    make_index(config)

if __name__ == "__main__":
    main()