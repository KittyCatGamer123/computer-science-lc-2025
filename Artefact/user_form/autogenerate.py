### Script used to automatically generate user data
import random

# Get the parent directory (Project)
# Add the parent directory to sys.path
# As seen in data_collect.py
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import utils

user_options = utils.read_json("user_form/user_form_options.json")

result = []
simulations = 200

for id in range(0, simulations+1):
    new_item = {"Id": id + 1000}

    for key in user_options.keys():
        new_item[key] = random.choice(user_options[key])

    result.append(new_item)

utils.write_json("user_form/user_data.json", result)