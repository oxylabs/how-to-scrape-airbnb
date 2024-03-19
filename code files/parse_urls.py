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
