#!/usr/bin/env python3
"""
Fetch RSS feeds and extract article information.
"""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import ssl

# Disable SSL verification for feedparser (workaround for macOS certificate issues)
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


def fetch_feed(feed_url: str, feed_title: str, category: str, hours: int = 24, target_date: str = None) -> List[Dict]:
    """
    Fetch a single RSS feed and extract recent articles.

    Args:
        feed_url: RSS feed URL
        feed_title: Feed title
        category: Feed category
        hours: Number of hours to look back for articles
        target_date: Target date in YYYY-MM-DD format (optional)

    Returns:
        List of article dictionaries
    """
    try:
        feed = feedparser.parse(feed_url)

        if feed.bozo and not feed.entries:
            print(f"Warning: Failed to parse feed {feed_title}: {feed_url}", file=sys.stderr)
            return []

        # Calculate cutoff time based on target_date or hours
        if target_date:
            # Parse target date and set time range to exactly that day
            target_dt = datetime.strptime(target_date, '%Y-%m-%d')
            # Start of target day
            start_of_day = target_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            # End of target day
            end_of_day = target_dt.replace(hour=23, minute=59, second=59, microsecond=999999)
            cutoff_time = start_of_day
            end_time = end_of_day
        else:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            end_time = datetime.now()

        articles = []

        for entry in feed.entries:
            # Parse published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])

            # Skip articles without date or outside the target range
            if not published:
                continue  # Skip articles without publish date
            if target_date:
                # When target_date is specified, filter to articles on that date
                if published < cutoff_time or published > end_time:
                    continue
            else:
                if published < cutoff_time:
                    continue  # Skip old articles

            # Extract article information
            article = {
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', entry.get('description', '')),
                'published': published.isoformat() if published else None,
                'source': feed_title,
                'category': category,
                'author': entry.get('author', ''),
            }

            articles.append(article)

        return articles

    except Exception as e:
        print(f"Error fetching {feed_title} ({feed_url}): {e}", file=sys.stderr)
        return []


def fetch_all_feeds(feeds: List[Dict[str, str]], hours: int = 24, target_date: str = None, max_workers: int = 10) -> List[Dict]:
    """
    Fetch all RSS feeds in parallel.

    Args:
        feeds: List of feed dictionaries from parse_opml
        hours: Number of hours to look back for articles
        target_date: Target date in YYYY-MM-DD format (optional)
        max_workers: Maximum number of parallel workers

    Returns:
        Combined list of all articles from all feeds
    """
    all_articles = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                fetch_feed,
                feed['xmlUrl'],
                feed['title'],
                feed['category'],
                hours,
                target_date
            ): feed for feed in feeds
        }

        for future in as_completed(futures):
            feed = futures[future]
            try:
                articles = future.result()
                all_articles.extend(articles)
                print(f"Fetched {len(articles)} articles from {feed['title']}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing {feed['title']}: {e}", file=sys.stderr)

    # Sort by published date (newest first)
    all_articles.sort(key=lambda x: x['published'] or '', reverse=True)

    return all_articles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch RSS feeds and extract articles')
    parser.add_argument('feeds_json', help='JSON file containing feed list from parse_opml')
    parser.add_argument('--window', type=int, default=24, help='Time window in hours (default: 24)')
    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD)')
    args = parser.parse_args()

    with open(args.feeds_json, 'r') as f:
        feeds = json.load(f)

    articles = fetch_all_feeds(feeds, hours=args.window, target_date=args.date)

    # Output as JSON
    print(json.dumps(articles, indent=2, ensure_ascii=False))
