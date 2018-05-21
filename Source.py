import requests
import json
import csv

URL = "https://api.spacexdata.com/v2/launches"
r = requests.get(url=URL)


json_launches = r.json()
launches_parsed = json.loads(r.text)

print(launches_parsed)