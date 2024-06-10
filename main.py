import requests
from bs4 import BeautifulSoup
import feedparser
import os
import csv
from xml.etree import ElementTree as ET
import collections
import pandas as pd
import numpy as np


def download_opml(opml_path):
    """Reads the OPML file and returns its content."""
    try:
        with open(opml_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(
            f"Error: OPML file not found at '{opml_path}'. Please check the path."
        )
        return None  # Return None to indicate failure


def opml_to_xml(opml_content):
    """Extracts RSS feed URLs from the OPML content."""
    if not opml_content:  # Handle None value from download_opml
        return []

    soup = BeautifulSoup(opml_content, 'xml')
    feeds = []
    for outline in soup.find_all('outline', type='rss'):
        yield outline['xmlUrl']
    return feeds


def xml_to_entity(feed_url):
    parsed_feed = feedparser.parse(feed_url)

    Entity = collections.namedtuple('Entity', ['title', 'link', 'summary'])
    for xml in parsed_feed.entries:
        yield Entity(xml.title, xml.link, xml.summary)


def entity_to_dataframe(df):
    pass


def save_feed_content(feed_url, output_dir):
    parsed_feed = feedparser.parse(feed_url)
    feed_title = parsed_feed.feed.title

    # Format the XML
    root = ET.Element("feed")
    for entry in parsed_feed.entries:
        item = ET.SubElement(root, "item")
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "description").text = entry.summary

    xml_string = ET.tostring(root, encoding='utf-8')
    xml = bytes_to_string_replace_and_back(xml_string)
    pretty_xml = BeautifulSoup(xml, 'xml').prettify()
    # Save to file
    with open(f"{output_dir}/{feed_title}.xml", "w", encoding='utf-8') as file:
        file.write(pretty_xml)
        print(f"Saved RSS file: {output_dir}/{feed_title}.xml")

    return pretty_xml


def replace_gt_lt(text):
    """Replaces '&gt;' and '&lt;' with '>' and '<' respectively in a given text."""

    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("&amp;", "&")
    return text


def bytes_to_string_replace_and_back(byte_data):

    string_data = byte_data.decode("utf-8")  # Convert bytes to string
    string_data = replace_gt_lt(string_data)
    return string_data


def write_rss_to_csv(feed_url):
    with open('my_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        parsed_feed = feedparser.parse(feed_url)
        feed_title = parsed_feed.feed.title

        #root = ET.Element("feed")

        # Write the header row
        writer.writerow(['FeedTitle', 'Title', 'Link', 'Summary'])
        writer.writerow([feed_title])
        for entry in parsed_feed.entries:
            #item = ET.SubElement(root, "item")
            writer.writerow([entry.title])
            writer.writerow([entry.link])
            writer.writerow([entry.summary])


def clean_entity(entity):
    pass


if __name__ == "__main__":
    opml_path = "rss/feedly_rss.opml"
    output_dir = "feed_outputs"
    os.makedirs(output_dir, exist_ok=True)

    opml_content = download_opml(opml_path)
    for rss_xml in opml_to_xml(opml_content):
        try:
            save_feed_content(rss_xml, output_dir)

            # df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            #...                    columns=['a', 'b', 'c'])
            titles = []
            links = []
            summaries = []
            for entity in xml_to_entity(rss_xml):
                titles.append(entity.title)
                links.append(entity.link)
                summaries.append(entity.summary)

            rss_data = {'Title': titles, 'Link': links, 'Summary': summaries}
            df = pd.DataFrame(data=rss_data)
            print(f"\ndf: {df}")

        except Exception as e:
            print(f"\nUnable to process feed_url: {e}\n")
