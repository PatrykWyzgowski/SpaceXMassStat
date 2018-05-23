import requests
import json
import pandas as pd
from collections import OrderedDict

def nested_to_dict(json):
    flattened_to_dict = {}

    def decompose(to_be_flattened, col_name=''):
        if type(to_be_flattened) is dict:
            for key in to_be_flattened:
                decompose(to_be_flattened[key], col_name + key + '_')
        elif type(to_be_flattened) is list:
            counter = 0
            for key in to_be_flattened:
                decompose(key, col_name + str(counter) + '_')
                counter=counter+1

        else:
            flattened_to_dict[col_name[:-1]] = to_be_flattened

    decompose(json)
    return flattened_to_dict
URL = "https://api.spacexdata.com/v2/launches"
r = requests.get(url=URL)
##ss
launches_parsed = json.loads(r.text)

newer = [nested_to_dict(index) for index in launches_parsed]

#df_from_records = pd.DataFrame.from_records(newer)
#df.to_csv('dataframe.csv')
fajnal = [OrderedDict(dic) for dic in newer]
df_final = pd.DataFrame.from_records(fajnal,index='flight_number')
df_final.to_csv('df_final.csv')

masses = pd.DataFrame(columns=['launch_year'])
masses['launch_year'] = df_final['launch_year']
masses['total_payload_mass'] = df_final['rocket_second_stage_payloads_0_payload_mass_kg'].fillna(0) + df_final['rocket_second_stage_payloads_1_payload_mass_kg'].fillna(0)
masses['mass_returned'] = df_final['rocket_second_stage_payloads_0_mass_returned_kg'].fillna(0)
#masses = masses[(masses.T != 0).any()]
masses.drop(masses[masses['total_payload_mass'] == 0].index, inplace=True)

print(masses)