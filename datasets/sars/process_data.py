"""
Script for processing sars_2003_complete_dataset_clean.csv into format for model.
"""

import csv
from datetime import date

# Earliest date in the dataset
base_date = date(2003, 3, 17)

compiled_data = {}
with open("./sars_2003_complete_dataset_clean.csv", 'r') as file:
    reader = csv.reader(file)
    # Skip headers
    next(reader)
    for row in reader:
        # Calculate time index
        components = row[0].split('-')
        calc_date = date(int(components[0]), int(components[1]), int(components[2]))
        t = (calc_date - base_date).days
        # If time index already in dictionary, add current cases to that time index
        if t in compiled_data:
            compiled_data[t] += int(row[2])
        # Else create time index in dictionary with current cases
        else:
            compiled_data[t] = int(row[2])
# Split dictionary into ordered array of keys and values
keys, values = zip(*compiled_data.items())

with open('processed_sars.csv', 'w', encoding='UTF8', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)
    # write initial population
    # according to https://www.theguardian.com/environment/interactive/2011/oct/24/how-big-worlds-population-born
    writer.writerow(["6292314517"])
    # write daily births in population
    # from https://www.infoplease.com/us/population/live-births-and-birth-rates-year
    writer.writerow([str(4089950 / 365.25)])
    # write daily deaths in population
    # from https://data.worldbank.org/indicator/SP.DYN.CDRT.IN
    writer.writerow([str(8.426 / 10000 * 6292314517)])
    # write total processed case numbers
    for i in range(len(keys)):
        writer.writerow([keys[i], values[i]])

    print("Processing complete!")
