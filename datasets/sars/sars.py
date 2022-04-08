import csv
from datetime import date

# Earliest date in the dataset
base_date = date(2003, 3, 17)

compiled_data = {}
with open('sars_2003_complete_dataset_clean.csv', 'r') as file:
    reader = csv.reader(file)
    # Skip headers
    next(reader)
    for row in reader:
        # Calculate time index
        components = row[0].split('-')
        calc_date = date(int(components[0]), int(components[1]), int(components[2]))
        t = (calc_date - base_date).days
        if t in compiled_data:
            compiled_data[t] += int(row[2])
        else:
            compiled_data[t] = int(row[2])

keys, values = zip(*compiled_data.items())

with open('processed_sars.csv', 'w') as f:
    # create the csv writer
    writer = csv.writer(f)

    for i in range(len(keys)):
        print(keys[i], values[i])
        writer.writerow(f'{keys[i]}, {values[i]}')
