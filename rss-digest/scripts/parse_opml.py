#!/usr/bin/env python3
"""
Parse OPML file to extract RSS feed URLs.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict
import sys


def parse_opml(opml_path: str) -> List[Dict[str, str]]:
    """
    Parse OPML file and extract RSS feed information.

    Args:
        opml_path: Path to the OPML file

    Returns:
        List of dictionaries containing feed information:
        - title: Feed title
        - xmlUrl: RSS feed URL
        - category: Feed category (if available)
    """
    try:
        tree = ET.parse(opml_path)
        root = tree.getroot()

        feeds = []

        # Find all outline elements that have xmlUrl attribute
        for outline in root.findall('.//outline[@xmlUrl]'):
            feed = {
                'title': outline.get('title', outline.get('text', 'Unknown')),
                'xmlUrl': outline.get('xmlUrl'),
                'category': outline.get('category', 'Uncategorized')
            }

            # Try to get category from parent outline
            parent = root.find(f".//outline[@xmlUrl='{feed['xmlUrl']}']/..")
            if parent is not None and parent.get('text'):
                feed['category'] = parent.get('text')

            feeds.append(feed)

        return feeds

    except ET.ParseError as e:
        print(f"Error parsing OPML file: {e}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print(f"OPML file not found: {opml_path}", file=sys.stderr)
        return []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_opml.py <opml_file>", file=sys.stderr)
        sys.exit(1)

    feeds = parse_opml(sys.argv[1])

    print(f"Found {len(feeds)} feeds", file=sys.stderr)
    for feed in feeds:
        print(f"  [{feed['category']}] {feed['title']}: {feed['xmlUrl']}", file=sys.stderr)

    # Output JSON to stdout
    import json
    print(json.dumps(feeds, indent=2, ensure_ascii=False))
