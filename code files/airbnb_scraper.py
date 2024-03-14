### airbnb_scraper.py
import asyncio
from scrape_20_urls import scrape_search
from parse_urls import parse


async def main():
    urls = await scrape_search()
    await parse(urls)

if __name__ == "__main__":
    asyncio.run(main())
