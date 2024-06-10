## can i somehow get its rss feeds in python?

Absolutely! You can extract RSS feed URLs from an .opml file using Python. Here's how:

**1. Use an XML Parser (xml.etree.ElementTree):**

```python
import xml.etree.ElementTree as ET

def get_rss_feeds(opml_file):
    tree = ET.parse(opml_file)
    root = tree.getroot()

    rss_feeds = []
    for outline in root.iter('outline'):
        if outline.attrib.get('type') == 'rss':
            rss_feeds.append(outline.attrib['xmlUrl'])

    return rss_feeds

# Example usage:
opml_file = "subscriptions.opml"
rss_feeds = get_rss_feeds(opml_file)
print(rss_feeds)
```

**Explanation:**

1. Import the `xml.etree.ElementTree` module.
2. Define a function `get_rss_feeds` that takes the OPML file path as input.
3. Parse the OPML file using `ET.parse`.
4. Get the root element of the XML tree.
5. Iterate over all `outline` elements in the tree.
6. If an outline has the attribute `type="rss"`, extract the `xmlUrl` attribute (the RSS feed URL) and add it to the `rss_feeds` list.
7. Return the list of RSS feed URLs.

**2. Use a Library (feedparser or listparser):**

- **feedparser:**  Although primarily for parsing RSS feeds, it can also handle OPML files. You'd iterate over the entries and look for elements with `type="rss"`.
- **listparser:** Specifically designed to parse subscription lists, including OPML.

**Additional Considerations:**

- **Error Handling:** Implement error handling (e.g., file not found, invalid XML) to make your code more robust.
- **OPML Structure:** OPML files can have different structures. If your file isn't standard, adjust the XML parsing logic accordingly.

Let me know if you'd like a more detailed example using `feedparser` or `listparser`, or need help adapting this to a non-standard OPML structure.