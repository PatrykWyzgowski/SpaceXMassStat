import requests
import json
from nestedToDict import nested_to_dict
import csv

URL = "https://api.spacexdata.com/v2/launches"
r = requests.get(url=URL)


json_launches = r.json()
launches_parsed = json.loads(r.text)

print(nested_to_dict(json_launches))
print(launches_parsed)