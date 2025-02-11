# How to Scrape Airbnb Listing Data With Python



[![Oxylabs promo code](https://raw.githubusercontent.com/oxylabs/product-integrations/refs/heads/master/Affiliate-Universal-1090x275.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5)](https://discord.gg/eWsVUJrnG5)

See this in-depth article to learn how to easily scrape Airbnb listings with Python while using Oxylabs’ [Airbnb Scraper API](https://oxylabs.io/products/scraper-api/web/airbnb) to bypass blocks and interruptions. 

You can find more information on this topic in our [blog post](https://oxylabs.io/blog/how-to-scrape-airbnb).

- [1. Install prerequisites](#1-install-prerequisites)
- [2. Get a free API trial and test your connection](#2-get-a-free-api-trial-and-test-your-connection)
  * [Send a test request](#send-a-test-request)
- [3. Import the libraries](#3-import-the-libraries)
- [4. Store API credentials and Airbnb listing URLs](#4-store-api-credentials-and-airbnb-listing-urls)
- [5. Create the payload](#5-create-the-payload)
- [6. Create parsing instructions](#6-create-parsing-instructions)
- [7. Create coroutines to process API jobs asynchronously](#7-create-coroutines-to-process-api-jobs-asynchronously)
  * [Submit a job](#submit-a-job)
  * [Check job status](#check-job-status)
  * [Get job results](#get-job-results)
  * [Process jobs](#process-jobs)
- [8. Save results to JSON](#8-save-results-to-json)
- [9. Bring everything together](#9-bring-everything-together)
- [Scrape Airbnb search page](#scrape-airbnb-search-page)
  * [1. Build the Airbnb search results scraper](#1-build-the-airbnb-search-results-scraper)
  * [2. Combine Airbnb listing and URL scrapers](#2-combine-airbnb-listing-and-url-scrapers)
  * [3. Scrape more listings by scrolling the page](#3-scrape-more-listings-by-scrolling-the-page)


## 1. Install prerequisites

Start by installing Python from the [official website](https://www.python.org/downloads/) if you don’t have it already. Additionally, we recommend using an Integrated Development Environment (IDE) like PyCharm or VS Code for easier development and debugging processes. Then, install the required Python libraries for this project:

```bash
pip install asyncio, aiohttp, requests
```

The [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://docs.aiohttp.org/en/stable/) modules will be used to make asynchronous requests and thus speed up the scraping process. Additionally, the [requests](https://requests.readthedocs.io/en/latest/) library will be used to send a simple test request.

## 2. Get a free API trial and test your connection

Head to the [Oxylabs dashboard](https://dashboard.oxylabs.io/en/?_gl=1*1u40pf6*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.) and claim your **7-day free trial** for [Web Scraper API](https://oxylabs.io/products/scraper-api/web) which includes Airbnb Scraper API. See the steps here on how to get your free trial when logged in to the dashboard.

Web Scraper API comes with a [worldwide proxy pool](https://developers.oxylabs.io/scraper-apis/web-scraper-api/all-domains?_gl=1*1u40pf6*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.#geo_location), a [Headless Browser](https://oxylabs.io/features/headless-browser), a [Custom Parser](https://oxylabs.io/features/custom-parser), [batch queries](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods/push-pull?_gl=1*2vw07*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.#batch-query), and other smart features for block-free web scraping. As a result, you won’t need any additional Python libraries like Beautiful Soup, Selenium, or Puppeteer since dynamic page rendering, human-like requests, and data parsing will be done via Web Scraper API.

### Send a test request

```python
import requests
from pprint import pprint

payload = {
    "source": "universal",
    "url": "https://www.airbnb.com/rooms/639705836870039306?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1437197361&search_mode=flex_destinations_search&check_in=2024-06-28&check_out=2024-07-03&source_impression_id=p3_1708944446_F%2FuHvpf5A7Gvt8Pi&previous_page_section_name=1000",
    "geo_location": "United States",
    "render": "html"
}

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"), # Replace with your API credentials
    json=payload
)

pprint(response.json())
```

If you see a `status_code` of `200` within the response, your scraping job has been executed successfully.

## 3. Import the libraries

The next step to scrape Airbnb data is to use and import the following libraries:

```python
import json, asyncio, aiohttp
from aiohttp import BasicAuth
```

## 4. Store API credentials and Airbnb listing URLs

```python
USERNAME, PASSWORD = "USERNAME", "PASSWORD"

urls = [
   "https://www.airbnb.com/rooms/639705836870039306?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1437197361&search_mode=flex_destinations_search&check_in=2024-06-28&check_out=2024-07-03&source_impression_id=p3_1708944446_F%2FuHvpf5A7Gvt8Pi&previous_page_section_name=1000",
   "https://www.airbnb.com/rooms/685374557739707093?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1514770868&search_mode=flex_destinations_search&check_in=2024-03-17&check_out=2024-03-22&source_impression_id=p3_1708944446_iBXKC59AR9NTQc4y&previous_page_section_name=1000",
   "https://www.airbnb.com/rooms/51241506?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1264515417&search_mode=flex_destinations_search&check_in=2024-04-07&check_out=2024-04-12&source_impression_id=p3_1708944446_zo%2FqBnbRPhn7zqAr&previous_page_section_name=1000",
]
```

## 5. Create the payload

```python
payload = {
    "source": "universal",
    "url": None,
    "geo_location": "United States",
    "user_agent_type": "desktop",
    "render": "html",
    "browser_instructons": [],
    "parse": True,
    "parsing_instructions": {}
}
```
Note that the `url` parameter is set to `None` since the Python scraper you’ll build will assign the target URLs dynamically. Moreover, if you want to make sure that elements load before the scraper initiates, you can use [browser instructions](https://developers.oxylabs.io/scraper-apis/headless-browser/browser-instructions-beta?_gl=1*k5omra*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.) to `wait_for_element`:

```python
    "browser_instructons": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "xpath",
                "value": "//div[@data-section-id='HOST_PROFILE_DEFAULT']"
            },
            "timeout_s": 30
        }
    ],
```

See the [documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api?_gl=1*k5omra*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.) to learn more about the available Web Scraper API parameters and their purpose.

## 6. Create parsing instructions

Copy this code into a new Python file and then save the payload into a separate `listing_payload.json` file to keep the scraper code shorter:


```python
import json

payload = {
    "source": "universal",
    "url": None,
    "geo_location": "United States",
    "user_agent_type": "desktop",
    "render": "html",
    "browser_instructons": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "xpath",
                "value": "//div[@data-section-id='HOST_PROFILE_DEFAULT']"
            },
            "timeout_s": 30
        }
    ],
    "parse": True,
    "parsing_instructions": {
        "titles": {
            "title_one": {
                "_fns": [
                    {
                        "_fn": "xpath_one",
                        "_args": ["//span/h1/text()"]
                    }
                ]
            },
            "title_two": {
                "_fns": [
                    {
                        "_fn": "xpath_one",
                        "_args": ["//div[contains(@data-section-id, 'OVERVIEW')]//h2/text()"]
                    }
                ]
            }
        },
        "pricing": {
            "price_per_night": {
                "_fns": [
                    {
                        "_fn": "xpath_one",
                        "_args": ["//span[@class='_tyxjp1']/text()", "//span[@class='_1y74zjx']/text()"]
                    }
                ]
            },
            "price_total": {
                "_fns": [
                    {
                        "_fn": "xpath_one",
                        "_args": ["//span/span[@class='_j1kt73']/text()"]
                    }
                ]
            }
        },
        "host_url": {
            "_fns": [
                {
                    "_fn": "xpath_one",
                    "_args": ["//div[contains(@data-section-id, 'HOST')]//a/@href"]
                }
            ]
        },
        "overall_rating": {
            "_fns": [
                {
                    "_fn": "xpath_one",
                    "_args": ["//*[contains(text(), 'Rated')]/following::div[1]/text()"]
                }
            ]
        },
        "reviews": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": ["//div[contains(@data-section-id, 'REVIEWS')]//div[@role='listitem']"]
                }
            ],
            "_items": {
                "rating": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[contains(@class, 'c5dn5hn')]/span/text()"]
                        },
                        {"_fn": "amount_from_string"}
                    ]
                },
                "date": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//div[contains(@class, 's78n3tv')]/text()"]
                        }
                    ]
                },
                "review": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [".//span[contains(@class, 'lrl13de')]/text()"]
                        }
                    ]
                }
            }
        },
        "images": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": ["//picture//*[@data-original-uri]/@data-original-uri"]
                }
            ]
        }
    }
}

with open("listing_payload.json", "w") as f:
    json.dump(payload, f, indent=4)
```

Then replace the `payload` in your main scraper file with the following lines:

```python
payload = {}
with open("listing_payload.json", "r") as f:
    payload = json.load(f)
```

If you want to scrape more data points from Airbnb listing pages, you can find a [payload file](code%20files/listing_payload_more_data.json) that achieves this in the `code files` folder.


## 7. Create coroutines to process API jobs asynchronously

### Submit a job

Oxylabs’ APIs support [batch processing](https://developers.oxylabs.io/scraper-apis/getting-started/integration-methods/push-pull?_gl=1*152wuc5*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.#batch-query) of `query` or `url` parameter values. Therefore, you can send a single request to process up to 1000 Airbnb URLs with the same scraping and parsing instructions. So, let’s define an asynchronous coroutine which will return job IDs for each submitted Airbnb URL:

```python
async def submit_job(payload):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.post("https://data.oxylabs.io/v1/queries/batch", json=payload) as response:
            try:
                r = await response.json()
                ids = [query['id'] for query in r["queries"]]
                print(ids)
                return ids
            except Exception as e:
                print(f"Error has occurred in {e}: {r}")
```

> [!IMPORTANT]
> Make sure not to exceed the free trial’s _rate limit_. Use up to `10` URLs; otherwise, the API will return the “Too many requests” [response code](https://developers.oxylabs.io/scraper-apis/getting-started/response-codes?_gl=1*5sfdi3*_gcl_au*MTQ0Mzk1NzUwNy4xNzA4OTM5Mzk5LjcxNjg3MzQ0My4xNzA5NzM2ODIxLjE3MDk3MzY4MjE.). The try-except block will print this error in your terminal. If you want to bypass this rate limit, head to the [pricing page](https://oxylabs.io/products/scraper-api/web/pricing) and pick a plan that suits you.

### Check job status

```python
async def check_job_status(job_id):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.get(f"https://data.oxylabs.io/v1/queries/{job_id}") as response:
            return (await response.json())["status"]
```

### Get job results

```python
async def get_job_results(job_id):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.get(f"https://data.oxylabs.io/v1/queries/{job_id}/results") as response:
            return (await response.json())["results"][0]["content"]
```
### Process jobs

```python
async def process_job(job_id, url, results_list):
    await asyncio.sleep(5)

    while True:
        status = await check_job_status(job_id)

        if status == "done":
            print(f"Job {job_id} done.")
            results = await get_job_results(job_id)
            results["listing_url"] = url
            results_list.append(results)
            break

        elif status == "failed":
            print(f"Job {job_id} failed.")
            break

        await asyncio.sleep(5)
```
## 8. Save results to JSON

```python
async def save_to_json(results_list):
    with open("parsed_listings.json", "a") as f:
        json.dump(results_list, f, indent=4)
```

## 9. Bring everything together

```python
async def parse(urls):
    payload["url"] = urls
    job_ids = await submit_job(payload)

    results_list = []

    await asyncio.gather(*(process_job(job_id, url, results_list) for job_id, url in zip(job_ids, urls)))  
    await save_to_json(results_list)

    print("Airbnb URLs parsed.")
```

Finally, add the main check to run the Python file when it’s called directly. Here’s the full code snippet that scrapes and parses public Airbnb listing data:

```python
### parse_urls.py
import json, asyncio, aiohttp
from aiohttp import BasicAuth

USERNAME, PASSWORD = "username", "password" # Replace with your API credentials

urls = [
   "https://www.airbnb.com/rooms/639705836870039306?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1437197361&search_mode=flex_destinations_search&check_in=2024-06-28&check_out=2024-07-03&source_impression_id=p3_1708944446_F%2FuHvpf5A7Gvt8Pi&previous_page_section_name=1000",
   "https://www.airbnb.com/rooms/685374557739707093?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1514770868&search_mode=flex_destinations_search&check_in=2024-03-17&check_out=2024-03-22&source_impression_id=p3_1708944446_iBXKC59AR9NTQc4y&previous_page_section_name=1000",
   "https://www.airbnb.com/rooms/51241506?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1264515417&search_mode=flex_destinations_search&check_in=2024-04-07&check_out=2024-04-12&source_impression_id=p3_1708944446_zo%2FqBnbRPhn7zqAr&previous_page_section_name=1000",
]

payload = {}
with open("listing_payload.json", "r") as f:
    payload = json.load(f)

async def submit_job(payload):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.post("https://data.oxylabs.io/v1/queries/batch", json=payload) as response:
            try:
                r = await response.json()
                ids = [query['id'] for query in r["queries"]]
                print(ids)
                return ids
            except Exception as e:
                print(f"Error has occurred in {e}: {r}")

async def check_job_status(job_id):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.get(f"https://data.oxylabs.io/v1/queries/{job_id}") as response:
            return (await response.json())["status"]

async def get_job_results(job_id):
    async with aiohttp.ClientSession(auth=BasicAuth(USERNAME, PASSWORD)) as session:
        async with session.get(f"https://data.oxylabs.io/v1/queries/{job_id}/results") as response:
            return (await response.json())["results"][0]["content"]

async def process_job(job_id, url, results_list):
    await asyncio.sleep(5)
    while True:
        status = await check_job_status(job_id)
        if status == "done":
            print(f"Job {job_id} done.")
            results = await get_job_results(job_id)
            results["listing_url"] = url
            results_list.append(results)
            break
        elif status == "failed":
            print(f"Job {job_id} failed.")
            break
        await asyncio.sleep(5)

async def save_to_json(results_list):
    with open("parsed_listings.json", "a") as f:
        json.dump(results_list, f, indent=4)

async def parse(urls):
    payload["url"] = urls
    job_ids = await submit_job(payload)
    results_list = []
    await asyncio.gather(*(process_job(job_id, url, results_list) for job_id, url in zip(job_ids, urls)))  
    await save_to_json(results_list)
    print("Airbnb URLs parsed.")

if __name__ == "__main__":
    asyncio.run(parse(urls))
```
Below you can see the JSON output of one of the scraped and parsed Airbnb listings:

```json
[
    {
        "images": [
            "https://a0.muscache.com/pictures/miso/Hosting-639705836870039306/original/a6e9e75e-8fe3-44d9-bd1b-9c20e111f09b.jpeg",
            "https://a0.muscache.com/pictures/miso/Hosting-639705836870039306/original/78a13367-2edd-4ad6-83f3-09c468cd2389.jpeg",
            "https://a0.muscache.com/pictures/miso/Hosting-639705836870039306/original/cca081b9-b868-4dbe-bdd2-585b3dd3b96a.jpeg",
            "https://a0.muscache.com/pictures/miso/Hosting-639705836870039306/original/7c553d75-b316-4961-920a-92c6327b1287.jpeg",
            "https://a0.muscache.com/pictures/miso/Hosting-639705836870039306/original/36a1d733-cea9-4802-bd96-f4a81a93c941.jpeg"
        ],
        "titles": {
            "title_one": "Private Rooftop Hidden Gem Studio",
            "title_two": "Entire rental unit in New York, United States"
        },
        "pricing": {
            "price_total": "$2,840",
            "price_per_night": "$478\u00a0"
        },
        "reviews": [
            {
                "date": "2 weeks ago",
                "rating": 5,
                "review": "Located in the heart of New York City, these apartments offer a prime location with easy access to everything you need. The highlight is definitely the amazing terrace, perfect for enjoying the city skyline. Henry, the host, is exceptionally proactive, providing excellent communication and clear instructions throughout the stay. A top choice for anyone looking for a comfortable and convenient stay in NYC."
            },
            {
                "date": "2 weeks ago",
                "rating": 5,
                "review": "Great location, easy to find the apartment"
            },
            {
                "date": "2 weeks ago",
                "rating": 1,
                "review": "Although the rooftop was very special, there was significant clanging noise from the heating pipes that made sleeping impossible.  We left after the first night, as Henry was not able to solve the problem.  Walls were also paper thin and could hear the conversations of neighbors.  Can't recommend."
            },
            {
                "date": "3 weeks ago",
                "rating": 5,
                "review": "Great midtown location near everything!"
            },
            {
                "date": "3 weeks ago",
                "rating": 5,
                "review": "Henry\u2019s home was absolutely gorgeous. Skyview\u2019s of surrounding buildings and the Empire State building right in your backyard was just breathtaking."
            },
            {
                "date": "3 weeks ago",
                "rating": 5,
                "review": "This place was perfect! It was in a great location and exactly as described. Henry was very communicative and quick to respond."
            }
        ],
        "host_url": "/users/show/461252637",
        "overall_rating": "4.84",
        "parse_status_code": 12000,
        "listing_url": "https://www.airbnb.com/rooms/639705836870039306?adults=1&category_tag=Tag%3A8536&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1437197361&search_mode=flex_destinations_search&check_in=2024-06-28&check_out=2024-07-03&source_impression_id=p3_1708944446_F%2FuHvpf5A7Gvt8Pi&previous_page_section_name=1000"
    }
]
```

## Scrape Airbnb search page

### 1. Build the Airbnb search results scraper

By default, the Airbnb website loads the first 20 listings on the search page. If you want to load more listings, you must scroll the page, which we'll show how to do later. To scrape an Airbnb search page, you need to instruct the Headless Browser to wait until the 20th listing loads, and then collect the URLs of those 20 Airbnb listings:

```python
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
```
As mentioned earlier, if you’re using the free API trial, make sure to provide up to 10 URLs so you don’t exceed the free trial’s rate limit.

### 2. Combine Airbnb listing and URL scrapers

To simplify the process, you can create another Python file that’ll import the `scrape_20_urls.py` and `parse_urls.py` files and run these scrapers together:

```python
### airbnb_scraper.py
import asyncio
from scrape_20_urls import scrape_search
from parse_urls import parse


async def main():
    urls = await scrape_search()
    await parse(urls)

if __name__ == "__main__":
    asyncio.run(main())
```
Remember to empty the `urls` list in the original `parse_urls.py` file so that it could be populated with newly scraped URLs after running the `scrape_20_urls.py` file.

### 3. Scrape more listings by scrolling the page

If you want to **increase the number of Airbnb listings** from 20 to around 250, you can instruct the browser to scroll the page by 1000 pixels, wait for 1 second, and then, after doing it 6 times – click the button that says “Show more.” Afterward, instruct the browser to scroll the page 20 more times:

```python
### scrape_250_urls.py

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
```
Evidently, Oxylabs’ solution makes the data scraping process significantly straightforward and scalable. In case you want to build a truly custom Airbnb scraper without Oxylabs’ API, you may want to use a headless browser like [Puppeteer to bypass anti-scraping systems](https://oxylabs.io/blog/puppeteer-tutorial) and consider implementing [proxy servers](https://oxylabs.io/proxy-server).
