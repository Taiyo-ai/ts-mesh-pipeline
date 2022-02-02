# 3rd
from gdacs.api import GDACSAPIReader
import json

# own
from dependencies.utils.utils import write_json_file


def get_data():
    """
        Gets GDACS information from the last 7 days (max time available information)
    """

    client = GDACSAPIReader()
    print("Scrapping from https://www.gdacs.org/xml/rss_7d.xml")
    events = client.latest_events(historical="7d")

    json_data = json.dumps(events)

    write_json_file('scraped_metadata.json', 'scraped_metadata', json_data)
