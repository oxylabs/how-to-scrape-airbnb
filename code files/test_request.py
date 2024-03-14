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
