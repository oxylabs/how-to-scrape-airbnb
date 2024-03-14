### scrape_20_urls.py
import asyncio, aiohttp, json

USERNAME, PASSWORD = "username", "password" # Replace with your API credentials

payload = {
    "source": "universal",
    "url": "https://www.airbnb.com/",
    "geo_location": "United States",
    "render": "html",
    "browser_instructons": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "xpath",
                "value": "//div[@data-testid='card-container']/a"
            },
            "timeout_s": 30
        }
    ],
    "parse": True,
    "parsing_instructions": {
        "links": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": ["//div[@data-testid='card-container']/a/@href"]
                }
            ]
        }
    }
}

async def scrape_search():
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.post("https://realtime.oxylabs.io/v1/queries", json=payload) as response:
            hrefs = (await response.json())["results"][0]["content"]["links"]
            urls = ["https://www.airbnb.com" + url for url in hrefs]
            with open("20_airbnb_urls.json", "w") as f:
                json.dump(urls, f, indent=4)
                print("Airbnb URLs saved.")
            return urls

if __name__ == "__main__":
    asyncio.run(scrape_search())
