import seaborn as sns
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

root_dir = Path(__file__).parents[1]

class EnergyCharts:
    sns.set_style()

    def __init__(self):
        self.heating_2011 = pd.read_csv(
            root_dir / 'data/vinkovci_grijanje_2011.csv'
        )
        self.electricity_2011 = pd.read_csv(
            root_dir / 'data/vinkovci_struja_2011.csv'
        )

    def heat_by_source(self):
        colname = 'potrošnja_toplinske_energije(kWh)'
        data = self.heating_2011

        data = data.groupby('energent').sum().reset_index()
        colors = sns.color_palette('pastel')[0:5]
        chart = plt.pie(
            data[colname],
            colors=colors,
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
        colors = sns.color_palette('pastel')[0:5]
        chart = plt.pie(
            data[colname],
            colors=colors,
            labels=data['nadkategorija'],
            autopct='%.0f%%'
        )
        plt.savefig(
            root_dir / 'charts/{}'.format(title),
            dpi=300,
            bbox_inches='tight'
        )
        return chart
