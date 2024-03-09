import pandas as pd
from us_state import state_to_abbrev

new_csv = []

with open('data/2023_Gaz_counties_national.txt', 'r') as in_file:
    lines = (line.split("\t") for line in in_file if line)
    lines.__next__()
    for line in lines:
        county = line[3].replace(" County", "")
        state = line[0]
        area = int(float(line[6])+float(line[7]))
        lat = float(line[8])
        lon = float(line[9])
        new_csv.append([','.join([county, state]), area, lat, lon])

new_csv = pd.DataFrame(new_csv, columns=['county', 'area', 'lat', 'lon'])
new_csv.to_csv('data/county_area.csv', index=False)

# %%
# clean population data
pop = pd.read_csv('data/co-est2022-pop.csv')
new_csv = []

# remove period before every county name
for i in range(len(pop)):
    county, state = pop['Geographic Area'][i].replace('.', '').split(', ')
    county = county.replace(' County', '')
    new_csv = new_csv + \
        [[','.join([county, state_to_abbrev[state]]),
          pop['2022'][i].replace(',', '')]]

new_csv = pd.DataFrame(new_csv, columns=['county', 'population'])
new_csv.to_csv('data/county_pop.csv', index=False)
