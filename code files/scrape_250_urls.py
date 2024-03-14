### scrape_250_urls.py
import asyncio, aiohttp, json

USERNAME, PASSWORD = "username", "password" # Replace with your API credentials

payload = {
    "source": "universal",
    "url": "https://www.airbnb.com/?tab_id=home_tab&refinement_paths%5B%5D=/homes&search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2023-07-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&search_type=category_change&category_tag=Tag:8522",
    "geo_location": "Canada",
    "render": "html",
    "browser_instructions": [
        {"type": "scroll", "x": 0, "y": 1000},
        {"type": "wait", "wait_time_s": 1}
    ] * 6 + [
        {"type": "click", "selector": {"type": "xpath", "value": "//button[text()='Show more']"}},
        {"type": "wait", "wait_time_s": 5}
    ] + [
        {"type": "scroll", "x": 0, "y": 1000},
        {"type": "wait", "wait_time_s": 1}
    ] * 20,
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
            with open("250_airbnb_urls.json", "w") as f:
                json.dump(urls, f, indent=4)
                print("Airbnb URLs saved.")
            return urls

if __name__ == "__main__":
    asyncio.run(scrape_search())
