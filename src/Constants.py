from dataclasses import dataclass
@dataclass
class Constants:
    population_2011 = 35312
    diesel_ton_mwh = 11.9
    petrol_ton_mwh = 12.3
    lpg_ton_mwh = 13.1
    gas_ton_mwh = 13.3

    co2_electricity_mwh_ton = 0.234
    co2_diesel_mwh_ton = 0.267
    co2_petrol_mwh_ton = 0.249
    co2_lpg_mwh_ton = 0.227
    co2_natgas_mwh_ton = 0.202
    co2_wood_mwh_ton = 0
    co2_heatoil_mwh_ton = 0.264