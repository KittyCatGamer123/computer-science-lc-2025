import matplotlib.pyplot as plt

# Get the parent directory (Project)
# Add the parent directory to sys.path
# As seen in data_collect.py
import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import utils

DATA = utils.read_json("compiled_data.json")

def graph_consumer_prices() -> None:
    data_key_list = ["ConsumerPriceMortgageInterest", "ConsumerPriceGoods"]
    key_list_len = len(data_key_list)

    for n, key in enumerate(data_key_list):
        plt.subplot(100 + (key_list_len * 10) + (n + 1))
        plt.title(utils.split_by_capitals(key))

        x_axis = []
        y_axis = []
        for n in DATA["ConsumerPriceMortgageInterest"]:
            x_axis.append(f"{n['Year']}Q{n['Quarter']}")
            y_axis.append(n["Value"])

        plt.plot(x_axis, y_axis)

    plt.show()

def graph_occupations(year: int) -> None:
    occupation_data = DATA["EmploymentLevelsAndOccupations"]
    occupations_for_year = utils.search_dict(occupation_data, "Year", year)

    if (occupations_for_year == []):
        print("No data available for year", year)
        return

    labels = []
    values = []
    for index in range(1, 10):
        occupation = utils.search_dict(occupations_for_year, "Index", str(index))[0]
        labels.append(occupation["Title"])
        values.append(occupation["Value"])
    
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels)
    plt.title(f"Employment Levels and Occupations for Year {year}")
    plt.show()

graph_consumer_prices()