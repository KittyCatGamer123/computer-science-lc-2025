import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('agg')

# Get the parent directory (Project)
# Add the parent directory to sys.path
# As seen in data_collect.py
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import utils
DATA = utils.read_json("compiled_data.json")

# Graphs the Consumer Prices from the compiled_data.json
# Creates line graph

def graph_consumer_prices() -> plt.Figure:
    data_key_list = ["ConsumerPriceMortgageInterest", "ConsumerPriceGoods"]
    key_list_len = len(data_key_list)
    
    fig, ax = plt.subplots()
    plt.clf()

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
            year_label = "'" + str(year)[2:]
            
            if year_label not in ticks_labels:
                ticks_indicies.append(index)
                ticks_labels.append(year_label)

        plt.xticks(ticks_indicies, ticks_labels)
        plt.plot(x_axis, y_axis)
        
    return plt.gcf()

# Graphs the Occupations from the compiled_data.json
# Creates pie chart

def graph_occupations(year: int) -> plt.Figure:
    if (type(year) != int):
        print(f"Invalid type for year {year}; Please use integers only.")
        return None
    
    occupation_data: list[dict] = DATA["EmploymentLevelsAndOccupations"]
    occupations_for_year: list[dict] = utils.search_dict(
        occupation_data, "Year", year)

    if (occupations_for_year == []):
        print("No data available for year", year)
        return None

    labels: list[str] = []
    values: list[str] = []
    
    for index in range(1, 10):
        occupation: dict = utils.search_dict(
            occupations_for_year, "Index", str(index))[0]
        labels.append(occupation["Title"])
        values.append(occupation["Value"])

    fig, ax = plt.subplots()
    plt.clf()
    ax.pie(values, labels=labels)

    plt.title(f"Employment Levels and Occupations for Year {year}")
    fig.set_size_inches(9, 4)
    
    return plt.gcf()

# Creates a line graph of Employment of a job over time
# Sector: The Sector object to search for in compiled data

def graph_employment_trend(sector: str, year_min: int = 0, year_max: int = 9999) -> None:
    year_min = int(year_min)
    year_max = int(year_max)
    
    if (type(sector) != str):
        print(f"Invalid type for sector {sector}; Please use strings only.")
        return None
    
    job_data = utils.search_dict(DATA["Employment"], "Sector", sector)
    all_employees_job_data = utils.search_dict(job_data, "Type", "All employees")
    
    if all_employees_job_data == []:
        print("Cannot find job", sector)
        return None

    job_data_filtered: list[dict] = []
    
    for job in all_employees_job_data:
        if (job['Year'] >= year_min) and (job['Year'] <= year_max):
            job_data_filtered.append(job)

    labels = []
    values = []
    ticks_indicies = []
    ticks_labels = []
    
    fig, ax = plt.subplots()
    plt.clf()

    for index, job in enumerate(job_data_filtered):
        year = job['Year']
        labels.append(f"{year}Q{job['Quarter']}")
        values.append(job['Value'])
        year_label = "'" + str(year)[2:]
            
        if year_label not in ticks_labels:
            ticks_indicies.append(index)
            ticks_labels.append(year_label)

    plt.xticks(ticks_indicies, ticks_labels)
    plt.plot(labels, values)
    plt.title(f"Employment Trend for\n{sector}")
    
    return plt.gcf()


# Creates a line graph of Weekly Earnings of a job over time
# Sector: The Sector object to search for in compiled data

def graph_weekly_earnings_trend(sector: str, year_min: int = 0, year_max: int = 9999):
    year_min = int(year_min)
    year_max = int(year_max)
    
    if (type(sector) != str):
        print(f"Invalid type for sector {sector}; Please use strings only.")
        return None
    
    job_data = utils.search_dict(DATA["AvgWeeklyEarnings"], "Sector", sector)
    all_employees_job_data = utils.search_dict(job_data, "Type", "All employees")
    
    if all_employees_job_data == []:
        print("Cannot find job", sector)
        return None

    job_data_filtered: list[dict] = []
    
    for job in all_employees_job_data:
        if (job['Year'] >= year_min) and (job['Year'] <= year_max):
            job_data_filtered.append(job)

    labels = []
    values = []
    ticks_indicies = []
    ticks_labels = []
    
    fig, ax = plt.subplots()
    plt.clf()

    for index, job in enumerate(job_data_filtered):
        year = job['Year']
        labels.append(f"{year}Q{job['Quarter']}")
        values.append(job['Value'])
        year_label = "'" + str(year)[2:]
            
        if year_label not in ticks_labels:
            ticks_indicies.append(index)
            ticks_labels.append(year_label)

    plt.xticks(ticks_indicies, ticks_labels)
    plt.plot(labels, values)
    plt.title(f"Average Weekly Earnings for\n{sector}")
    
    return plt.gcf()
    
### Unit Testing
# graph_occupations(2015)   => Visualisation success
# graph_occupations("2014") => "No data available" despite being int param??
# graph_occupations(-2.5)   => Same as above
# graph_occupations([2015]) => Same as above


## Returns bar graph of Gender rates in user_data.json
def user_data_gender():
    return user_data_freqbar("Gender", "Gender")

## Returns bar graph of Age rates in user_data.json
def user_data_age():
    return user_data_freqbar("Age", "Age Groups")

## Returns bar graph of Annual Income rates in user_data.json
def user_data_payrange():
    return user_data_freqbar("AnnualIncome", "Annual Income")

## Takes in a key from a user_data dictionary and uses its frequencies to display a bar chart.
def user_data_freqbar(key: str, name: str):
    user_data: list[dict] = utils.read_json("user_form/user_data.json")
    user_survey_options = utils.read_json("user_form/user_form_options.json")

    labels = user_survey_options[key] # [Male, Female, ...]
    item_frequency = {}               # { Male: #, Female: #, ... }

    for val in user_data:
        item_key = val[key]
        if item_key not in item_frequency:
            item_frequency[item_key] = 0
        
        item_frequency[item_key] += 1

    values = [item_frequency[x] for x in labels]

    # Adds an \n to labels with dashes in them
    for index in range(0, len(labels)):
        label: str = labels[index]
        if "-" in label:
            label_split = label.split("-")
            labels[index] = f"{label_split[0]}-\n{label_split[1]}"
    
    fig, ax = plt.subplots()
    
    ax.bar(labels, values, width=1, edgecolor="white")
    plt.title(name)

    return plt.gcf()