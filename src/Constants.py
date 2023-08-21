from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class Constants:
    population_2011 = 35312
    diesel_ton_mwh = 11.9
    petrol_ton_mwh = 12.3
    lpg_ton_mwh = 13.1
    gas_ton_mwh = 13.3

    co2_diesel_mwh_ton = 0.267
    co2_petrol_mwh_ton = 0.249
    co2_lpg_mwh_ton = 0.227
    co2_natgas_mwh_ton = 0.202
    co2_wood_mwh_ton = 0
    co2_heatoil_mwh_ton = 0.264

    co2_electricity_mwh_ton_2011: float
    co2_electricity_mwh_ton_2019: float

    density_heatoil = 840  # kg/m3
    upper_heat_value_heatoil = 12.611  # kwh/kg

    upper_heat_value_natgas = 12.75  # kwh/m3

    # household fuel share
    hh_heat_natgas_share = 0.5773
    hh_heat_heatoil_share = 0.0389
    hh_heat_wood_share = 0.2783
    hh_heat_electricity_share = 0.1056

    commercial_heat_natgas_share = 0.6609
    commercial_heat_heatoil_share = 0.0683
    commercial_heat_wood_share = 0.2460
    commercial_heat_electricity_share = 0.0248

    specific_consumption_diesel_2005 = 0.0663  # l/km
    specific_consumption_petrol_2005 = 0.0781  # l/km

    specific_consumption_diesel_2000 = 0.0691  # l/km
    specific_consumption_petrol_2000 = 0.0813  # l/km
    specific_consumption_total_2000 = 0.078075 # l/km


    def __init__(self):
        current_script_path = Path(__file__)
        parent_dir = current_script_path.parents[1]
        file_path = parent_dir / "data" / "public_data/JRC-COM-NEEFE_1990-2020.xlsx"

        df = pd.read_excel(file_path, sheet_name=1, skiprows=1, engine='openpyxl')
        # set the value for Croatia for the year 2011 and 2019
        self.co2_electricity_mwh_ton_2011 = df.loc[df["Unnamed: 0"] == "Croatia", 2011].values[0]
        self.co2_electricity_mwh_ton_2019 = df.loc[df["Unnamed: 0"] == "Croatia", 2019].values[0]
