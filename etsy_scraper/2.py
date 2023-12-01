import json

with open('data.json', 'r') as json_file:
    loaded_dict = json.load(json_file)

print(len(list(set(loaded_dict['products_links']))))