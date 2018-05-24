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
launches_parsed = json.loads(r.text)
flat_launches_list = [nested_to_dict(index) for index in launches_parsed]

ordered_flat_launches_list = [OrderedDict(dic) for dic in flat_launches_list]
df_launches = pd.DataFrame.from_records(ordered_flat_launches_list, index='flight_number')
df_launches.to_csv('df_final.csv')

masses = pd.DataFrame(columns=['launch_year'])
masses['launch_year'] = df_launches['launch_year']
masses['total_payload_mass'] = df_launches['rocket_second_stage_payloads_0_payload_mass_kg'].fillna(0) + df_launches['rocket_second_stage_payloads_1_payload_mass_kg'].fillna(0)
masses['mass_returned'] = df_launches['rocket_second_stage_payloads_0_mass_returned_kg'].fillna(0)
masses.drop(masses[masses['total_payload_mass'] == 0].index, inplace=True)

grouped = pd.DataFrame(columns=['count'])
grouped['count'] = masses.groupby('launch_year').count()['total_payload_mass']
grouped['sum'] = masses.groupby('launch_year').sum()['total_payload_mass']
grouped['mean'] = masses.groupby('launch_year').mean()['total_payload_mass'].round(2)
grouped['median'] = masses.groupby('launch_year').median()['total_payload_mass']

grouped.to_csv('aggregated_data.csv')