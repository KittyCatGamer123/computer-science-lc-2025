import csv
import io
import requests
import json

# Get the parent directory (Project)
# Add the parent directory to sys.path
import sys, os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import utils

# Make a HTTP Request with a URL.
# url: The URL to make a request to (string)
# Will return a string of content, or will end the program if it fails
def make_request(url: str) -> str:
    try:
        request_response = requests.get(url)
        request_response.encoding = 'utf-8-sig'
        request_response.raise_for_status()
        return request_response.content
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to get response from URL:\n\t{err}")
        exit()
    
    except Exception as err:
        print(f"Unknown error occurred:\n\t{err}")
        exit()

# Takes a string and turns it into a dictionary for each header of the csv
# data: The CSV content to turn into this dict.
# included_headers: List of specified headers that are wanted to be included in the data (all lowercase)
# Will return lists embedded within a dictionary e.g. {"Header1":[], "Header2":[]}
def format_csv(data: bytes, included_headers: list) -> dict:
    data_as_string = data.decode('utf-8-sig')
    csv_reader = csv.reader(io.StringIO(data_as_string))
    headers = next(csv_reader)
    result = {}
    
    # Iterate over each row until there isn't anything to read
    while True:
        try:
            row = next(csv_reader)
            for index, value in enumerate(row):
                key = headers[index]
                
                if key.lower() not in included_headers:
                    continue
                
                if key not in result.keys():
                    result[key] = []
                
                if value.isnumeric(): value = float(value)
                result[key].append(value)
        
        except StopIteration:
            return result

# Wrapper function to go from the URL Pool object to the Dictionary
# url_pool_data: URL Pool object supplied from urls_pool.json
def get_csv_dict(url_pool_data: dict) -> dict:
    raw_data = make_request(url_pool_data["URLs"])
    return format_csv(raw_data, url_pool_data["IncludedHeaders"])


UNIT_CONVERSION_RATE = {
    "Number": 1,
    "Euro": 1,
    "Hour": 1,
    "Thousand": 1000,
    "Euro Million": 1e+6
}

MONTH_TO_YEAR_QUARTER = {
    "January": 1,
    "February": 1,
    "March": 1,
    "April": 2,
    "May": 2,
    "June": 2,
    "July": 3,
    "August": 3,
    "September": 3,
    "October": 4,
    "November": 4,
    "December": 4
}

if __name__ == "__main__":
    # urls_pool.json is a hardcoded JSON file that contains the urls to for data to be analysed,
    # including its URL and the headers to include.
    URLS_LIST = utils.read_json("data_collection/urls_pool.json")["URLs"]
    
    # The Output variable is what will be written to the JSON file that we are going to use
    # for showing the data visually, after the final touch-up to data is applied.
    Output = {
        "Employment": [],
        "AvgWeeklyEarnings": [],
        "AvgHourlyEarnings": [],
        "BenefitInKind": [],
        "EmploymentLevelsAndOccupations": [],
        "ConsumerPriceGoods": [],
        "ConsumerPriceMortgageInterest": []
    }
    
    ### Employment Occupations
    EmploymentLevelsAndOccupations = get_csv_dict(URLS_LIST["EmploymentLevelsAndOccupations"])
    
    for index in range(0, len(EmploymentLevelsAndOccupations["UNIT"])):
        job_title: str = EmploymentLevelsAndOccupations["Detailed Occupational Group"][index]
        year, quarter = EmploymentLevelsAndOccupations["Quarter"][index].split("Q")
        
        value = EmploymentLevelsAndOccupations["VALUE"][index]
        unit = EmploymentLevelsAndOccupations["UNIT"][index]
        if value == '': value = 0
        
        Output["EmploymentLevelsAndOccupations"].append({
            "Title": job_title[job_title.index(" ")+1:],
            "Index": job_title[:job_title.index(" ")],
            "Year": int(year),
            "Quarter": int(quarter),
            "Unit": unit,
            "Value": float("{:.2f}".format(float(value) * UNIT_CONVERSION_RATE[unit]))
        })
    
    ### Consumer Prices
    ConsumerPrices = get_csv_dict(URLS_LIST["ConsumerPrices"])
    
    for index in range(0, len(ConsumerPrices["VALUE"])):
        job_sub_index = ConsumerPrices["Selected Sub Indices"][index]
        
        # Just skip the indicies we won't be analysing
        if (job_sub_index != "Goods") and (job_sub_index != "Mortgage Interest"): continue
        if (ConsumerPrices["UNIT"][index] != "Base Dec 2023=100"): continue
        
        value = ConsumerPrices["VALUE"][index]
        if value == '': continue
        
        output_key = "ConsumerPriceGoods" if job_sub_index == "Goods" else "ConsumerPriceMortgageInterest"
        
        # Split month into year and quarter
        month_split = ConsumerPrices["Month"][index].split(" ")
        year = month_split[0]
        quarter = MONTH_TO_YEAR_QUARTER[month_split[1]]
        
        Output[output_key].append({
            "Year": int(year),
            "Quarter": int(quarter),
            "Value": float("{:.2f}".format(float(value) * UNIT_CONVERSION_RATE[unit]))
        })
    
    AvgEarningsHoursEmployment = get_csv_dict(URLS_LIST['AvgEarningsHoursEmployment'])
    EmploymentStatsLabel: dict[str, str] = {
        "Employment": "Employment",
        "Average Weekly Earnings": "AvgWeeklyEarnings",
        "Average Hourly Earnings": "AvgHourlyEarnings",
        "Average Hourly Benefit in Kind": "BenefitInKind"
    }
    
    for index in range(0, len(AvgEarningsHoursEmployment["Quarter"])):
        stat_label: str = AvgEarningsHoursEmployment["Statistic Label"][index]
        if stat_label not in EmploymentStatsLabel.keys():
            continue
        
        output_key = EmploymentStatsLabel[stat_label]
        year, quarter = AvgEarningsHoursEmployment["Quarter"][index].split("Q")
        
        value = AvgEarningsHoursEmployment["VALUE"][index]
        unit = AvgEarningsHoursEmployment["UNIT"][index]
        if value == '': value = 0
        
        
        Output[output_key].append({
            "Sector": AvgEarningsHoursEmployment["Economic Sector NACE Rev 2"][index],
            "Type": AvgEarningsHoursEmployment["Type of Employee"][index],
            "Year": int(year),
            "Quarter": int(quarter),
            "Value": float("{:.2f}".format(float(value) * UNIT_CONVERSION_RATE[unit]))
        })
        
    ### Write Output to a valid JSON file
    utils.write_json("compiled_data.json", Output)