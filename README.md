# Electrical Vehicle Market Analysis

Data exploration and analysis of the EV Market across US States.

## File Descriptions

- `graphs.ipynb`: Jupyter Notebook with all graphs
- `map.py`: code for generating heat map of EV population by county
- `ev_pop_station`: code for generating EV popultion vs Charge Port graphs
- `data/`: dataset files
- `utils/`: dataset cleaning and misc.
- `results/`: resulting figures saved

## Usage

1. `pip install -r requirements.txt`
2. Go to `graphs.ipynb` and run cells to see graph outputs

## Datasets

- [Alternative Fueling Station Counts by State](https://afdc.energy.gov/stations/states?count=total&include_temporarily_unavailable=false&date=)
- [Vehicle Registration Counts by State](https://afdc.energy.gov/vehicle-registration)
- [Area by State](https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area)
- Map data refs listed in `map.py`
