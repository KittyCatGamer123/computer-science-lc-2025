import matplotlib.pyplot as plt

# Get the parent directory (Project)
# Add the parent directory to sys.path
# As seen in data_collect.py
import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import utils

DATA = utils.read_json("compiled_data.json")

# Graphs the Consumer Prices from the compiled_data.json
# Creates line graph
def graph_consumer_prices() -> None:
    data_key_list = ["ConsumerPriceMortgageInterest", "ConsumerPriceGoods"]
    key_list_len = len(data_key_list)

    for i, key in enumerate(data_key_list):
        plt.subplot(100 + (key_list_len * 10) + (i + 1))
        plt.title(utils.split_by_capitals(key))

        x_axis = []
        y_axis = []
        
        ticks_indicies = []
        ticks_labels = []
        for index, n in enumerate(DATA["ConsumerPriceMortgageInterest"]):
            year = n['Year']
            x_axis.append(f"{year}Q{n['Quarter']}")
            y_axis.append(n["Value"])
            
            if str(year) not in ticks_labels:
                ticks_indicies.append(index)
                ticks_labels.append(str(year))

        plt.xticks(ticks_indicies, ticks_labels)
        plt.plot(x_axis, y_axis)

    plt.show()

# Graphs the Occupations from the compiled_data.json
# Creates pie chart
def graph_occupations(year: int) -> None:
    occupation_data: list[dict] = DATA["EmploymentLevelsAndOccupations"]
    occupations_for_year: list[dict] = utils.search_dict(occupation_data, "Year", year)

    if (occupations_for_year == []):
        print("No data available for year", year)
        return

    labels: list[str] = []
    values: list[str] = []
    for index in range(1, 10):
        occupation: dict = utils.search_dict(occupations_for_year, "Index", str(index))[0]
        labels.append(occupation["Title"])
        values.append(occupation["Value"])
    
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels)
    plt.title(f"Employment Levels and Occupations for Year {year}")
    plt.show()