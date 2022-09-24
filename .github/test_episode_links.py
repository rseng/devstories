# Copyright @vsoch, 2022

import os
import sys
import requests
import tempfile
import shutil

import xml.etree.ElementTree as ET

here = os.path.dirname(os.path.abspath(__file__))


def test(url):
    assert requests.head(url).status_code == 200


def check_feed(url):
    """check integrity of episode links in the current feed."""
    # Retrieve latest XML of episodes
    res = requests.get(url)
    if res.status_code != 200:
        sys.exit(f"Issue getting {url}")

    # We will save to temporary file and load
    tmpdir = tempfile.mkdtemp()
    xmlfile = os.path.join(tmpdir, "episodes.rss")
    with open(xmlfile, "w") as fd:
        fd.write(res.text)

    # XML tree, posts are under rss->channel
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for i, episode in enumerate(root[0]):
        link = episode.find("link")
        if link is not None:
            print(f"Testing {link.text}")
            test(link.text)
        link = episode.find("enclosure")
        if link is None:
            continue
        link = link.get("url", None)
        if link:
            print(f"Testing {link}")
            test(link)

    # Cleanup
    shutil.rmtree(tmpdir)


def main():
    feed = "https://rseng.github.io/devstories/episodes.rss"
    check_feed(feed)


if __name__ == "__main__":
    main()
