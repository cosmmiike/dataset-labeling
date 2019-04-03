import os
import json

json_dir = os.path.dirname(os.path.abspath(__file__)) + '/static/labeling/json/'

with open(json_dir + 'sets.json') as json_file:
    sets = json.load(json_file)

sets_num = len(sets)
set_titles = list(sets.keys())

with open(json_dir + 'dataset.json') as json_file:
    data = json.load(json_file)

data_num = len(data['data'])

sets_output = dict()

for title in set_titles:
    sets_output[title] = list()

    for i, category in enumerate(sets[title]):
        sets_output[title].append({})
        sets_output[title][i]['category'] = category

        count = 0
        for image in data['data']:
            if image[title] == str(i):
                count += 1
                
        sets_output[title][i]['count'] = count

print(sets_output)
