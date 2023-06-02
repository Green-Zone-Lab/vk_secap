import seaborn as sns
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

root_dir = Path(__file__).parents[1]

class EnergyCharts:
    sns.set_style()

    def __init__(self):
        self.n_residents_2011 = 35.312
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

        petrol_spent = private_cars['procijenjena_potrošena_masa_benzina(t)'].sum()
        diesel_spent = private_cars['procijenjena_potrošena_masa_dizela(t)'].sum()
        unp_spent = private_cars['procijenjena_potrošena_masa_unp(t)'].sum()

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

        # convert city consumption in L to tonnes like in private data
        city_cars_petrol = city_cars.loc[
            city_cars["vrsta_goriva"] == "benzin"
        ]['potrošnja_goriva(l)'] * 0.00085
        city_cars_diesel = city_cars.loc[
            city_cars["vrsta_goriva"] == "dizel"
        ]['potrošnja_goriva(l)'] * 0.00072

        potrošnja = private_cars.loc[~private_cars["procijenjena_potrošnja_goriva(kWh)"].isna()]
        chart = plt.pie(
            potrošnja["procijenjena_potrošnja_goriva(kWh)"],
            colors=self.colors,
            labels=potrošnja["vrsta_prijevoza"],
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/gorivo_po_vrsti_prijevoza_2011.png',
            dpi=300,
            bbox_inches='tight'
        )
        return chart

    def energy_per_capita(self):
       toplinska_per_capita = self.heating_2011["potrošnja_toplinske_energije(kWh)"].sum() / self.n_residents_2011
       print(toplinska_per_capita)

