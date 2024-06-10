import requests
from bs4 import BeautifulSoup
import feedparser
import os
from xml.etree import ElementTree as ET

def download_opml(opml_path):
    """Reads the OPML file and returns its content."""
    try:
        with open(opml_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: OPML file not found at '{opml_path}'. Please check the path.")
        return None  # Return None to indicate failure

def extract_rss_feeds(opml_content):
    """Extracts RSS feed URLs from the OPML content."""
    if not opml_content:  # Handle None value from download_opml
        return []

    soup = BeautifulSoup(opml_content, 'xml')
    feeds = []
    for outline in soup.find_all('outline', type='rss'):
        feeds.append(outline['xmlUrl'])
    return feeds

def save_feed_content(feed_url, output_dir):
    """Fetches and saves the feed content as a formatted XML file."""
    parsed_feed = feedparser.parse(feed_url)
    feed_title = parsed_feed.feed.title

    root = ET.Element("feed")
    ET.SubElement(root, "title").text = feed_title

    for entry in parsed_feed.entries:
        item = ET.SubElement(root, "item")
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "description").text = entry.summary

    # Format the XML
    xml_string = ET.tostring(root, encoding='utf-8')
    xml = bytes_to_string_replace_and_back(xml_string)
    pretty_xml = BeautifulSoup(xml, 'xml').prettify()

    # Save to file
    with open(f"{output_dir}/{feed_title}.xml", "w", encoding='utf-8') as file:
        file.write(pretty_xml)
        print(f"Saved RSS file: {output_dir}/{feed_title}.xml")

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

    
if __name__ == "__main__":
    opml_path = "rss/feedly_rss.opml"
    output_dir = "feed_outputs"  

    os.makedirs(output_dir, exist_ok=True)

    opml_content = download_opml(opml_path)
    if opml_content:
        rss_feeds = extract_rss_feeds(opml_content)

        for feed_url in rss_feeds:
            try:
                save_feed_content(feed_url, output_dir)
            except Exception as e:
                print(f"\nUnable to process RSS file: {feed_url}: {e}\n")