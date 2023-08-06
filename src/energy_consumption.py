import seaborn as sns
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from src.Constants import Constants

root_dir = Path(__file__).parents[1]

constant = Constants()


class Energy2011:
    sns.set_style()

    def __init__(self):
        self.n_residents_2011 = 35312
        self.colors = sns.color_palette('pastel')[0:5]
        self.heating_2011 = pd.read_csv(
            root_dir / 'data/vinkovci_grijanje_2011.csv'
        )
        self.electricity_2011 = pd.read_csv(
            root_dir / 'data/vinkovci_struja_2011.csv'
        )
        self.city_cars_2011 = pd.read_csv(
            root_dir / 'data/gradska_vozila_2011.csv'
        )
        self.private_cars_2011 = pd.read_csv(
            root_dir / 'data/privatna_vozila_2011.csv'
        )

    def heat_by_source(self):
        colname = 'potrošnja_toplinske_energije(kWh)'
        data = self.heating_2011

        data = data.groupby('energent').sum().reset_index()
        chart = plt.pie(
            data[colname],
            colors=self.colors,
            labels=data['energent'],
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/toplina_po_energentu_2011.png',
            dpi=300,
            bbox_inches='tight'
        )
        return chart

    def energy_by_sector(self, source):
        if source == 'heat':
            colname = 'potrošnja_toplinske_energije(kWh)'
            data = self.heating_2011
            title = 'toplina_po_sektoru_2011.png'
        else:
            colname = 'potrošnja_električne_energije(kWh)'
            data = self.electricity_2011
            title = 'struja_po_sektoru_2011.png'

        data = data.groupby('nadkategorija').sum().reset_index()
        chart = plt.pie(
            data[colname],
            colors=self.colors,
            labels=data['nadkategorija'],
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/{}'.format(title),
            dpi=300,
            bbox_inches='tight'
        )
        return chart

    def gas_by_type(self):
        private_cars = self.private_cars_2011
        city_cars = self.city_cars_2011
        private_cars.fillna(0)
        city_cars_petrol = (city_cars.iloc[0]['potrošnja_goriva(l)'] * constant.petrol_litre_to_kwh)
        city_cars_diesel = (city_cars.iloc[1]['potrošnja_goriva(l)'] * constant.diesel_litre_to_kwh)

        petrol_spent = private_cars['procijenjena_potrošena_masa_benzina(t)'].sum() * constant.petrol_litre_to_kwh * constant.petrol_ton_to_litre
        diesel_spent = private_cars['procijenjena_potrošena_masa_dizela(t)'].sum() * constant.diesel_litre_to_kwh * constant.diesel_ton_to_litre
        unp_spent = private_cars['procijenjena_potrošena_masa_unp(t)'].sum() * constant.lpg_ton_to_litre * constant.lpg_litre_to_kwh

        petrol_spent = petrol_spent + city_cars_petrol
        diesel_spent = diesel_spent + city_cars_diesel

        chart = plt.pie(
            [petrol_spent, diesel_spent, unp_spent],
            colors=self.colors,
            labels=['benzin', 'dizel', 'ukapljeni naftni plin'],
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/vrsta_goriva_2011.png',
            dpi=300,
            bbox_inches='tight'
        )
        return chart

    def gas_by_category(self):
        city_cars = self.city_cars_2011
        private_cars = self.private_cars_2011
        private_cars = private_cars.fillna(0)
        city_cars['energy'] = (city_cars.iloc[0]['potrošnja_goriva(l)'] * constant.petrol_litre_to_kwh) \
                              + (city_cars.iloc[1]['potrošnja_goriva(l)'] * constant.diesel_litre_to_kwh)



        # convert city consumption in L to tonnes like in private data
        private_cars['energy'] = (private_cars[
                                       'procijenjena_potrošena_masa_benzina(t)'] * constant.petrol_ton_to_litre * constant.petrol_litre_to_kwh) \
                                 + (private_cars[
                                         'procijenjena_potrošena_masa_dizela(t)'] * constant.diesel_ton_to_litre * constant.diesel_litre_to_kwh) \
                                 + (private_cars[
                                         'procijenjena_potrošena_masa_unp(t)'] * constant.lpg_ton_to_litre * constant.lpg_litre_to_kwh)
        private_cars.loc[private_cars['vrsta_prijevoza'] == 'osobna_vozila', 'energy'] += city_cars['energy']
        consumption = private_cars.loc[~private_cars["procijenjena_potrošnja_goriva(kWh)"].isna()]
        consumption.loc[consumption['vrsta_prijevoza'] == 'taxi', 'energy'] = consumption.loc[
            consumption['vrsta_prijevoza'] == 'taxi'
            ]['potrošnja_dizelskog_goriva(l)'] * constant.diesel_litre_to_kwh

        threshold = 2
        consumption["percentage"] = 100 * consumption["energy"] / consumption["energy"].sum()
        small_categories = consumption["percentage"] < threshold
        consumption.loc[small_categories, "vrsta_prijevoza"] = "Taxi, autobusi, mopedi i motocikli"
        grouped_consumption = consumption.groupby("vrsta_prijevoza").sum()

        chart = plt.pie(
            grouped_consumption["energy"],
            colors=self.colors,
            labels=grouped_consumption.index,  # Use the index (vrsta_prijevoza) as labels
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/gorivo_po_vrsti_prijevoza_2011.png',
            dpi=300,
            bbox_inches='tight'
        )
        return chart
