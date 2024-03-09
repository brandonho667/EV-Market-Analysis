#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

file_path = 'data/historical-station-counts.xlsx'


def extract_charging_outlets(file_path, states):
    state_outlets_counts = {state: {} for state in states}

    for year in range(2016, 2023):
        # Load the sheet for the year
        data_year_full = pd.read_excel(file_path, sheet_name=str(year))

        for state in states:
            state_row = data_year_full[data_year_full.iloc[:, 0]
                                       == state].index[0]
            state_outlets = data_year_full.iloc[state_row, 4]
            state_outlets_count = int(state_outlets.split('|')[
                                      1].strip().replace(',', ''))
            state_outlets_counts[state][year] = state_outlets_count

    return state_outlets_counts


states = ['California', 'Florida', 'Texas', 'Washington', 'New York']

charging_outlets_counts = extract_charging_outlets(file_path, states)

# for state, counts in charging_outlets_counts.items():
#     print(f"{state}:")
#     for year, count in counts.items():
#         print(f"  {year}: {count} outlets")
#     print()

charging_outlets_data = {
    'Florida': [2091, 2508, 3027, 4562, 5564, 6748, 7818],
    'Texas': [2386, 2654, 3138, 4009, 4807, 5501, 6332],
    'Washington': [1791, 2136, 2573, 3206, 3817, 4325, 4533],
    'New York': [1677, 1952, 2562, 4531, 6134, 7646, 9535],
    'California': [13655, 16111, 21166, 27199, 34924, 41237, 43589]
}

ev_population_data = {'Florida': [11600, 15900, 27400, 40300, 58200, 95600, 168000],
                      'Texas': [11900, 16100, 24500, 38400, 52200, 80900, 149000],
                      'Washington': [14900, 21000, 30200, 40400, 50500, 66800, 104100],
                      'New York': [6100, 9400, 15500, 23000, 32600, 51900, 84700],
                      'California': [141500, 189700, 273500, 349700, 425300, 563100, 903600]}

land_area_data = {'Florida': 53625, 'Texas': 261232, 'Washington': 66456,
                  'New York': 47126, 'California': 155779}

colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan']

# In[12]:


def linear_func(x, k, b):
    return k * x + b


def plot_charge_ports():

    plt.figure(figsize=(14, 9))

    all_outlets = np.concatenate(list(charging_outlets_data.values()))
    min_x, max_x = min(all_outlets), max(all_outlets)
    x_vals_extended = np.linspace(min_x, max_x, 500)

    for i, (state, outlets) in enumerate(charging_outlets_data.items()):
        ev_population = ev_population_data[state]
        params, _ = curve_fit(linear_func, np.array(
            outlets), np.array(ev_population))
        k, b = params
        y_vals_extended = linear_func(x_vals_extended, k, b)
        plt.scatter(outlets, ev_population,
                    color=colors[i], label=f'{state} Data')
        plt.plot(x_vals_extended, y_vals_extended,
                 color=colors[i], label=f'{state} Fitted Curve (y = {k:.2f}x + ({b:.2f})')

    plt.title('EV Population vs Charging Outlets (2016-2022) for CA, FL, TX, WA, NY')
    plt.xlabel('Number of Charging Outlets')
    plt.ylabel('EV Population (in millions)')
    plt.legend()
    plt.grid(True)
    plt.show()


# In[13]:

def plot_charge_port_density():
    plt.figure(figsize=(14, 9))

    all_outlets_density = np.concatenate(
        [[outlets / land_area_data[state] for outlets in outlets] for state, outlets in charging_outlets_data.items()])
    min_x, max_x = min(all_outlets_density), max(all_outlets_density)
    x_vals_extended = np.linspace(min_x, max_x, 500)
    for i, (state, outlets) in enumerate(charging_outlets_data.items()):
        ev_population = ev_population_data[state]
        outlets_density = [outlets[i] / land_area_data[state]
                           for i in range(len(outlets))]
        params, _ = curve_fit(linear_func, np.array(
            outlets_density), np.array(ev_population))
        k, b = params
        y_vals_extended = linear_func(x_vals_extended, k, b)
        plt.scatter(outlets_density, ev_population,
                    color=colors[i], label=f'{state} Data')
        plt.plot(x_vals_extended, y_vals_extended,
                 color=colors[i], label=f'{state} Fitted Curve (y = {k:.2f}x + ({b:.2f})')

    plt.title(
        'EV Population vs Charging Outlets per Square Mile (2016-2022) for CA, FL, TX, WA, NY')
    plt.xlabel('Charging Outlets per Square Mile')
    plt.ylabel('EV Population (in millions)')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_ev_gasoline_ratio():
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]

    ratios_percent = {
        'California': [0.5194, 0.6734, 0.9547, 1.1972, 1.4348, 1.8455, 2.9093],
        'Florida': [0.0833, 0.1114, 0.1884, 0.2737, 0.3899, 0.6130, 1.0602],
        'Washington': [0.2796, 0.3779, 0.5385, 0.7199, 0.8879, 1.1533, 1.8422],
        'New York': [0.0609, 0.0940, 0.1555, 0.2315, 0.3296, 0.5130, 0.8481],
        'Texas': [0.0652, 0.0882, 0.1328, 0.1990, 0.2662, 0.3927, 0.7073]
    }

    colors = {'California': 'blue', 'Florida': 'green',
              'Washington': 'red', 'New York': 'orange', 'Texas': 'purple'}

    plt.figure(figsize=(10, 6))
    for state, color in colors.items():
        plt.plot(years, ratios_percent[state],
                 label=state, marker='o', color=color)

    plt.title('EV to Gasoline Vehicle Ratio by State (2016-2022)')
    plt.xlabel('Year')
    plt.ylabel('EV to Gasoline Vehicle Ratio (%)')
    plt.legend()
    plt.grid(True)
    plt.show()


# In[ ]:
