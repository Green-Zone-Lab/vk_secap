from dataclasses import dataclass

import numpy as np


@dataclass
class SupplementaryData:
    land_structure = {
        'Građevinska područja naselja': 0.25,
        'Izgrađene strukture van naselja': 0.1,
        'Ostale površine': 0.01,
        'Poljoprivredne površine': 0.33,
        'Šumske površine': 0.28,
        'Vodne površine': 0.03
    }

    land_building_share = {
        'Izgrađeni dio građevinskog područja': 73.25,
        'Neizgrađeni dio građevinskog područja': 26.75
    }

    arable_land_structure = {
        'Osobito vrijedno obradivo tlo': 49.7,
        'Vrijedno obradivo tlo': 477.44,
        'Ostala obradiva tla': 2.85,
    }

    arable_land_use = {
        'Oranica': 92.05,
        'Voćnjak': 7.63,
        'Livada': 0.14,
        'Pašnjak': 0.12,
        'Vinograd': 0.02,
        'Ostalo': 0.04,
    }

    water_shortages = {
        # first col average year
        # second col dry year
        'Kukuruz': [221.4, 437.6],
        'Šećerna repa': [254.5, 485.9],
        'Rajčica': [247.7, 460.9],
        'Jabuka': [329.9, 441.7],
        'Suncokret': [183.4, 337],
        'Krumpir': [205.5, 403.4],
        'Lucerna': [180.6, 388.7],
        'Paprika': [180.7, 332],
        'Grašak': [184.7, 304.8],
        'Mahune': [116.7, 218.2],
        'Kukuruz silažni': [50.5, 164.8],
    }

    hummus_per_county = {
        'Bjelovarsko-bilogorska': 1.78,
        'Brodsko-posavska': 1.8,
        'Istarska': 2.15,
        'Karlovačka': 2.44,
        'Koprivničko-križevačka': 1.54,
        'Krapinsko-zagorska': 2.23,
        'Ličko-senjska': 2.89,
        'Međimurska': 2.01,
        'Požeško-slavonska': 1.62,
        'Primorsko-goranska': 3.32,
        'Sisačko-moslovačka': 2.13,
        'Šibensko-kniska': 2.74,
        'Virovitičko-podravska': 1.53,
        'Vukovarsko-srijemska': 1.63,
        'Zadarska': 2.01,
        'Zagrebačka': 2.22
    }

    agri_employment_age = {
        #  first col county, second col vinkovci
        '<41': [23.65, 22.98],
        '41-45': [8.49, 9.09],
        '46-50': [9.84, 11.11],
        '51-55': [9.85, 8.33],
        '56-60': [12.14, 11.36],
        '61-65': [11.75, 11.61],
        '66-100': [24.27, 25.51],
    }

    employment_vinkovci = {
        'Prerađivačka industrija': 18.27,
        'Trgovina, popravak motornih vozila': 14.22,
        'Javna uprava': 12.93,
        'Zdravstvena zaštita i socijalna skrb': 11.48,
        'Građevinarstvo': 10.12,
        'Obrazovanje': 8.8,
        'Prijevoz i skladištenje': 5.47,
        'Poljoprivreda, šumarstvo i ribarstvo': 3.42,
        'Ostalo': 15.29
    }

    bdp_index_region = {
        'Vukovarsko-srijemska županija': 62.95,
        'Panonska Hrvatska': 67.3,
        'Sjeverna Hrvatska': 78.8,
        'Jadranska Hrvatska': 94.8,
        'Grad Zagreb': 173.7,
        'Republika Hrvatska': 100,
    }

    agri_education = {
        # first col county second vinkovci
        'Nema podataka': [24.09, 23.04],
        'Nezavršena škola': [2.28, 1.52],
        'Osnovna škola': [18.37, 6.08],
        'Srednja Škola': [45.07, 45.57],
        'Visoko obrazovanje': [9.65, 24.05],
    }

    turism_seasonality = {
        # cols: 2019, 2020, 2021, 2022
        'Siječanj': [1582, 2507, 1101, 2245],
        'Veljača': [2105, 3989, 1305, 2684],
        'Ožujak': [4345, 1762, 2057, 3726],
        'Travanj': [5974, 477, 2819, 7424],
        'Svibanj': [4807, 777, 4121, 6163],
        'Lipanj': [4668, 1987, 3138, 4942],
        'Srpanj': [3390, 2529, 2712, 3880],
        'Kolovoz': [3562, 2678, 3245, 4501],
        'Rujan': [6747, 3256, 4997, 8491],
        'Listopad': [np.nan, 2104, 3212, np.nan],
        'Studeni': [np.nan, 1999, 4636, np.nan],
        'Prosinac': [np.nan, 1384, 2816, np.nan],
    }

    precipitation = {
        # cols: 2019, 2020, 2021, 2022
        'Siječanj': [40.1, 18.7, 61.2, 6.6],
        'Veljača': [23.6, 37, 45.4, 30.7],
        'Ožujak': [14.8, 39.2, 34.5, 8.8],
        'Travanj': [112.9, 14.8, 55.2, 53.9],
        'Svibanj': [120.8, 56, 42.9, 52.6],
        'Lipanj': [77.1, 58.8, 11.8, 52.8],
        'Srpanj': [64.3, 53.3, 99.8, 9.1],
        'Kolovoz': [49.4, 65.5, 80.9, 53.5],
        'Rujan': [101.9, 18.2, 8.7, 106.9],
        'Listopad': [32.9, 75.2, 90.1, 20.5],
        'Studeni': [79.1, 19.7, 87.5, 92.5],
        'Prosinac': [54, 73, 86.1, 65.4],
    }

    arrivals_sleepovers = {
        # first cols arrival, second col sleepover
        2016: [23233, 43761],
        2017: [27492, 56508],
        2018: [26605, 53889],
        2019: [26554, 52332],
        2020: [11256, 23504],
        2021: [18741, 45782],
        2022: [27786, 57839],
    }

    employment_tourism = {
        2018: 2.25,
        2019: 2.33,
        2020: 2.28,
        2021: 2.36,
        2022: 2.37,
    }

    tourists_per_capita = {
        # first col tourists, second col sleepover
        2018: [1.88, 1.2],
        2019: [1.89, 1.2],
        2020: [1.54, 0.9],
        2021: [1.76, 1.1],
        2022: [1.93, 1.23],
    }






