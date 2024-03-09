# %%
import pandas as pd
import plotly.express as px
import numpy as np
from utils.us_state import state_to_abbrev

# %% [markdown]
# # Electric Vehicle Population Size by County
# Plot heat map of electric vehicles using [`Electric_Vehicle_Population_Size_History_By_County.csv`](https://www.autosinnovate.org/resources/electric-vehicle-sales-dashboard).
#
# ## Auxiliary Datasets:
# From [census.gov](census.gov) webistes.
#  - [`2023_Gaz_counties_national.txt`](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_counties_national.zip): location (lat/long) and area of each county
#  - [`co-est2022-pop.xlsx`](https://www2.census.gov/programs-surveys/popest/tables/2020-2022/counties/totals/co-est2022-pop.xlsx): population by county
#

# %%
# locations to csv


def plot_map():
    # %%
    ev_pop_large = pd.read_csv(
        'data/Electric_Vehicle_Population_Size_History_By_County.csv')
    ev_pop = pd.DataFrame()
    ev_pop['county'] = ev_pop_large['County']+','+ev_pop_large['State']
    ev_pop['ev'] = ev_pop_large['Electric Vehicle (EV) Total']
    ev_pop['non_ev'] = ev_pop_large['Non-Electric Vehicle Total']
    ev_pop['total'] = ev_pop_large['Total Vehicles']
    ev_pop['percent_ev'] = ev_pop_large['Percent Electric Vehicles']

    county_loc = pd.read_csv('data/county_area.csv')
    county_pop = pd.read_csv('data/county_pop.csv')

    # %%
    all_map = pd.merge(ev_pop, county_loc, on='county')
    all_map = pd.merge(all_map, county_pop, on='county')

    # %%
    radii = np.log(all_map.total)*2
    radii[radii < 1] = 1

    # %%
    # plot heatmap for percentage of electric vehicles
    fig = px.density_mapbox(all_map, lat='lat', lon='lon', z='percent_ev', radius=radii,
                            center=dict(lat=38, lon=-95.7129), zoom=3,
                            mapbox_style="open-street-map",
                            hover_data=['county', 'area',
                                        'percent_ev', 'population'],
                            labels={'percent_ev': 'Percent Electric Vehicles',
                                    'area': 'Area (sq mi)', 'population': 'Population', 'county': 'County'},
                            color_continuous_scale=px.colors.sequential.Viridis,
                            title='Percentage of Electric Vehicles by County in the US',
                            width=1000, height=600)

    fig.show()
