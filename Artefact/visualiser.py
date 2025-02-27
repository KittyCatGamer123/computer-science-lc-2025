import matplotlib.pyplot as plt

import utils

DATA = utils.read_json("compiled_data.json")

# data_key_list = ["ConsumerPriceMortgageInterest", "ConsumerPriceGoods"]
# key_list_len = len(data_key_list)

# for n, key in enumerate(data_key_list):
#     plt.subplot(100 + (key_list_len * 10) + (n + 1))
#     plt.title(key)

#     x_axis = []
#     y_axis = []
#     for n in DATA["ConsumerPriceMortgageInterest"]:
#         x_axis.append(f"{n['Year']}Q{n['Quarter']}")
#         y_axis.append(n["Value"])

#     plt.plot(x_axis, y_axis)

# plt.show()

def graph_occupations() -> None:
    OccupationData = DATA["EmploymentLevelsAndOccupations"]

    startYear = OccupationData[0]["Year"]
    endYear = OccupationData[-1]["Year"]

    for year in range(startYear, endYear+1):
        occupations_for_year = utils.search_dict(OccupationData, "Year", year)

        labels = []
        values = []
        for index in range(1, 10):
            occupation = utils.search_dict(occupations_for_year, "Index", str(index))[0]
            labels.append(occupation["Title"])
            values.append(occupation["Value"])
        
        
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels)

graph_occupations()