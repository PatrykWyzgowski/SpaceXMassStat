import requests
import json
#from nestedToDict import nested_to_dict
import csv

def nested_to_dict(json):
    flattened_to_dict = {}

    def flatten(to_be_flattened, col_name=''):
        if type(to_be_flattened) is dict:
            for key in to_be_flattened:
                flatten(to_be_flattened[key], col_name + key + '_')
        elif type(to_be_flattened) is list:
            counter = 0
            for key in to_be_flattened:
                flatten(key, col_name + str(counter) + '_')
                counter=counter+1

        else:
            flattened_to_dict[col_name[:-1]] = to_be_flattened

    flatten(json)
    return flattened_to_dict
URL = "https://api.spacexdata.com/v2/launches"
r = requests.get(url=URL)

launches_parsed = json.loads(r.text)

newer = [nested_to_dict(index) for index in launches_parsed]

#df = pd.DataFrame(newer, columns=newer[0].keys())
#CSVwritard(launches_parsed,'parsed.csv')
#df.to_csv('dataframe1.csv')
