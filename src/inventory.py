import seaborn as sns
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from Constants import Constants

root_dir = Path(__file__).parents[1]


class Inventory:
    def __init__(self, constants, year):
        color_palette = sns.color_palette()

        pd.set_option('display.float_format', lambda x: '%.1f' % x)

        self.co2_factors = {
            "Dizel": constants.co2_diesel_mwh_ton,
            "Benzin": constants.co2_petrol_mwh_ton,
            "UNP": constants.co2_lpg_mwh_ton,
            "prirodni plin": constants.co2_natgas_mwh_ton,
            "ogrjevno drvo": constants.co2_wood_mwh_ton,
            "lož ulje": constants.co2_heatoil_mwh_ton  # Corresponds to heat oil
        }
        if year == 2011:
            self.co2_factors["električna energija"] = constants.co2_electricity_mwh_ton_2011
        elif year == 2019:
            self.co2_factors["električna energija"] = constants.co2_electricity_mwh_ton_2019

        self.colors = {
            'lož ulje': color_palette[1],  # 'orange'
            'električna energija': color_palette[0],  # 'blue'
            'prirodni plin': color_palette[3],  # 'red'
            'ogrjevno drvo': color_palette[5],  # 'green'
            'Dizel': color_palette[8],
            'Benzin': color_palette[9],
            'UNP': color_palette[6],

            'stambeni objekti': color_palette[0],  # 'blue'
            'zgrade komercijalnog i uslužnog karaktera': color_palette[1],  # 'orange',
            'zgrade javne namjene': color_palette[2],  # 'green'

            'teretna i radna vozila': color_palette[6],
            'osobna vozila': color_palette[7],
            'ostalo': color_palette[8],
            'autobusni': color_palette[9],
            'mopedi i motocikli': color_palette[4],

        }

    def stacked_bar(self, data, log=False):
        sns.set_theme()
        sns.set_style()
        color_palette = sns.color_palette()

        self.colors = {
            'lož ulje': color_palette[1],  # 'orange'
            'električna energija': color_palette[0],  # 'blue'
            'prirodni plin': color_palette[3],  # 'red'
            'ogrjevno drvo': color_palette[5],  # 'green'
            'Dizel': color_palette[8],
            'Benzin': color_palette[9],
            'UNP': color_palette[6],

            'stambeni objekti': color_palette[0],  # 'blue'
            'zgrade komercijalnog i uslužnog karaktera': color_palette[1],  # 'orange',
            'zgrade javne namjene': color_palette[2],  # 'green'

            'teretna i radna vozila': color_palette[6],
            'osobna vozila': color_palette[7],
            'ostalo': color_palette[8],
            'autobusni': color_palette[9],
            'mopedi i motocikli': color_palette[4],

        }

        fig, ax = plt.subplots(figsize=(10, 6))
        try:
            colors = [self.colors[energent] for energent in data.columns]
            data.plot(kind='barh', stacked=True, ax=ax, width=0.5, color=colors)
            legend = ax.legend(fontsize='x-small', loc='upper left', bbox_to_anchor=(1, 1))
            plt.setp(legend.get_title(), fontsize='x-small')
        except AttributeError:
            data.plot(kind='barh', stacked=False, ax=ax, width=0.5)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        plt.rc('axes', labelsize='x-small')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')

        ax.set_xlabel("log Ukupna potrošnja energije (MWh)", fontsize=9)
        ax.set_ylabel("")

        #if log:
            #ax.set_xscale('log')

        return fig

    def compare_stacked_bar(self, data1, data2, year1, year2, log=False):
        sns.set_theme()
        sns.set_style()

        fig, ax = plt.subplots(figsize=(10, 6))

        # Merge the two dataframes side by side
        merged_data = pd.concat([data1, data2], axis=1, keys=['Year1', 'Year2'])

        # Get the colors for each energent
        try:
            colors1 = [self.colors[energent] for energent in data1.columns]
            colors2 = [self.colors[energent] for energent in data2.columns]

            # Plot the first year's data with slightly reduced alpha for distinction
            bars = merged_data['Year1'].plot(kind='barh', stacked=True, ax=ax, width=0.3, color=colors1, position=0, alpha=0.8, label=[f"{year1} - {col}" for col in data1.columns])
            for bar in bars.patches:
                bar.set_hatch('...')

            # Plot the second year's data
            merged_data['Year2'].plot(kind='barh', stacked=True, ax=ax, width=0.3, color=colors2, position=1, alpha=1.0, label=[f"{year2} - {col}" for col in data2.columns])
            legend_labels = [f"{year1} - {col}" for col in data1.columns] + [f"{year2} - {col}" for col in
                                                                             data2.columns]
            handles, _ = ax.get_legend_handles_labels()
            ax.legend(handles[:len(legend_labels)], legend_labels, fontsize='x-small', loc='upper left',
                      bbox_to_anchor=(1, 1))

        except AttributeError:
            bars = merged_data['Year1'].plot(kind='barh', stacked=False, ax=ax, width=0.3, position=0, alpha=0.8,
                                             label=f"{year1}")
            for bar in bars.patches:
                bar.set_hatch('...')
            merged_data['Year2'].plot(kind='barh', stacked=False, ax=ax, width=0.3, position=0, alpha=0.8,
                                  label=f"{year2}")

        ax.grid(axis='x', linestyle='--', alpha=0.7)
        plt.rc('axes', labelsize='x-small')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')
        ax.set_xlabel("log Ukupna potrošnja energije (MWh)", fontsize=9)
        ax.set_ylabel("")

        # if log:
        #     ax.set_xscale('log')

        return fig


    def pie(self, data):
        sns.set_theme()
        sns.set_style()
        color_palette = sns.color_palette()

        self.colors = {
            # fuels
            'lož ulje': color_palette[1],  # 'orange'
            'električna energija': color_palette[0],  # 'blue'
            'prirodni plin': color_palette[3],  # 'red'
            'ogrjevno drvo': color_palette[5],  # 'green'
            'Dizel': color_palette[8],
            'Benzin': color_palette[9],
            'UNP': color_palette[6],

            # buildings
            'stambeni objekti': color_palette[0],  # 'blue'
            'zgrade komercijalnog i uslužnog karaktera': color_palette[1],  # 'orange',
            'zgrade javne namjene': color_palette[2],  # 'green'

            # transport
            'teretna i radna vozila': color_palette[6],
            'osobna vozila': color_palette[7],
            'ostalo': color_palette[8],
            'autobusni': color_palette[9],
            'mopedi i motocikli': color_palette[4],

            # sectors
            'javna rasvjeta': color_palette[5],  # 'red
            'zgradarstvo': color_palette[7],
            'promet': color_palette[0],

        }

        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot.pie(
            autopct='%1.1f%%', startangle=90,
            colors=[self.colors[energent] for energent in data.index],
            ax=ax
        )
        ax.set_ylabel('')

        return fig

    def base_inventory(self, output_dir, heat, ele, trans, light):
        output_dir.mkdir(exist_ok=True)

        """heat data"""

        heat['potrošnja_energije(MWh)'] = heat['potrošnja_energije(kWh)'] / 1000
        heat['Emisije CO2 (t)'] = heat.apply(
            lambda row: row['potrošnja_energije(MWh)'] * self.co2_factors[row['energent']],
            axis=1
        )
        # tablica_1 = heat.pivot_table(
        #     index=['nadkategorija', 'kategorija', 'broj zgrada', 'ukupna_grijana_površina',
        #            'specifična_potrošnja_energije(kWh/m2)'],
        #     columns='energent',
        #     values='potrošnja_energije(MWh)',
        #     aggfunc='sum',
        #     fill_value=0
        # ).groupby('kategorija').sum()
        # tablica_1_co2 = heat.pivot_table(
        #     index=['nadkategorija', 'kategorija', 'broj zgrada', 'ukupna_grijana_površina',
        #            'specifična_potrošnja_energije(kWh/m2)'],
        #     columns='energent',
        #     values='Emisije CO2 (t)',
        #     aggfunc='sum',
        #     fill_value=0
        # ).groupby('kategorija').sum()

        # stacked bar for heat by sector and fuel
        heat_pivot = heat.pivot(index='kategorija', columns='energent', values='potrošnja_energije(MWh)').fillna(0)
        order = ['prirodni plin', 'lož ulje', 'ogrjevno drvo', 'električna energija']
        heat_pivot = heat_pivot[order]
        heat_pivot['Total'] = heat_pivot.sum(axis=1)
        heat_pivot = heat_pivot.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        heat_by_sector = self.stacked_bar(heat_pivot, log=True)
        heat_by_sector.savefig(output_dir / 'potrošnja_toplinske.png', dpi=300, bbox_inches='tight')

        # stacked bar for heat CO2 by sector and fuel
        heat_co2_pivot = heat.pivot(index='kategorija', columns='energent', values='Emisije CO2 (t)').fillna(0)
        order = ['prirodni plin', 'lož ulje', 'ogrjevno drvo', 'električna energija']
        heat_co2_pivot = heat_co2_pivot[order]
        heat_co2_pivot['Total'] = heat_co2_pivot.sum(axis=1)
        heat_co2_pivot = heat_co2_pivot.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        heat_co2_by_sector = self.stacked_bar(heat_co2_pivot, log=True)
        heat_co2_by_sector.savefig(output_dir / 'emisije_co2_toplinske.png', dpi=300, bbox_inches='tight')

        # heat pie by fuel
        heat_pie_1 = heat.groupby('energent')['potrošnja_energije(MWh)'].sum()
        heat_pie_1_fig = self.pie(heat_pie_1)
        heat_pie_1_fig.savefig(output_dir / 'potrošnja_toplinske_energent.png', dpi=300, bbox_inches='tight')

        # heat co2 pie by source
        heat_co2_pie_1 = heat.groupby('energent')['Emisije CO2 (t)'].sum().drop('ogrjevno drvo')
        heat_co2_pie_1_fig = self.pie(heat_co2_pie_1)
        heat_co2_pie_1_fig.savefig(output_dir / 'emisije_co2_toplinske_energent.png', dpi=300, bbox_inches='tight')

        # heat pie by consumer
        heat_pie_2 = heat.groupby('nadkategorija')['potrošnja_energije(MWh)'].sum()
        heat_pie_2_fig = self.pie(heat_pie_2)
        heat_pie_2_fig.savefig(output_dir / 'potrošnja_toplinske_sektor.png', dpi=300, bbox_inches='tight')

        # heat pie by
        heat_co2_pie_2 = heat.groupby('nadkategorija')['Emisije CO2 (t)'].sum()
        heat_co2_pie_2_fig = self.pie(heat_co2_pie_2)
        heat_co2_pie_2_fig.savefig(output_dir / 'emisije_co2_toplinske_sektor.png', dpi=300, bbox_inches='tight')

        """electricity data"""

        ele['potrošnja_energije(MWh)'] = ele['potrošnja_energije(kWh)'] / 1000
        ele['Emisije CO2 (t)'] = ele['potrošnja_energije(MWh)'] * self.co2_factors['električna energija']

        tablica_2 = ele.groupby('kategorija').sum()

        # total electricity consumption
        ele_bar = ele.groupby('kategorija')['potrošnja_energije(MWh)'].sum()
        ele_bar = ele_bar.sort_values(ascending=True).drop(columns=['Total'])
        ele_bar_fig = self.stacked_bar(ele_bar, log=True)
        ele_bar_fig.savefig(output_dir / 'potrošnja_električne.png', dpi=300, bbox_inches='tight')

        # electricity co2 emissions
        ele_co2_bar = ele.groupby('kategorija')['Emisije CO2 (t)'].sum()
        ele_co2_bar = ele_co2_bar.sort_values(ascending=True)
        ele_co2_bar_fig = self.stacked_bar(ele_co2_bar)
        ele_co2_bar_fig.savefig(output_dir / 'emisije_co2_električne.png', dpi=300, bbox_inches='tight')

        # pie charts
        ele_pie_1 = ele.groupby('nadkategorija')['potrošnja_energije(MWh)'].sum()
        ele_pie_1_fig = self.pie(ele_pie_1)
        ele_pie_1_fig.savefig(output_dir / 'potrošnja_električne_sektor.png', dpi=300, bbox_inches='tight')

        ele_co2_pie_1 = ele.groupby('nadkategorija')['Emisije CO2 (t)'].sum()
        ele_co2_pie_1_fig = self.pie(ele_co2_pie_1)
        ele_co2_pie_1_fig.savefig(output_dir / 'emisije_co2_električne_sektor.png', dpi=300, bbox_inches='tight')

        """transport data"""
        trans = trans.loc[trans['vrsta_prijevoza'] != 'taxi']
        trans = trans.fillna(0)
        trans['Dizel'] = trans['procijenjena_potrošena_masa_dizela(t)'] * constants.diesel_ton_mwh
        trans['Benzin'] = trans['procijenjena_potrošena_masa_benzina(t)'] * constants.petrol_ton_mwh
        trans['UNP'] = trans['procijenjena_potrošena_masa_unp(t)'] * constants.lpg_ton_mwh

        order = ['Dizel', 'Benzin', 'UNP']
        trans_pivot = trans.set_index('vrsta_prijevoza')
        trans_pivot = trans_pivot[order]
        trans_pivot['Total'] = trans_pivot.sum(axis=1)
        trans_pivot = trans_pivot.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        trans_pivot_fig = self.stacked_bar(trans_pivot)
        trans_pivot_fig.savefig(output_dir / 'potrošnja_energije_transport.png', dpi=300, bbox_inches='tight')

        trans_pie_1 = trans_pivot.sum(axis=1)
        trans_pie_1['ostalo'] = trans_pie_1['mopedi i motocikli'] + trans_pie_1['autobusni']
        trans_pie_1 = trans_pie_1.drop(['mopedi i motocikli', 'autobusni'])
        trans_pie_1_fig = self.pie(trans_pie_1)
        trans_pie_1_fig.savefig(output_dir / 'potrošnja_energije_transport_vrsta.png', dpi=300, bbox_inches='tight')

        trans_melted = trans_pivot.reset_index().melt(id_vars=['vrsta_prijevoza'],
                                                      value_vars=['Dizel', 'Benzin', 'UNP'],
                                                      var_name='energent',
                                                      value_name='potrošnja_energije(MWh)')

        trans_pie_2 = trans_melted.groupby('energent')['potrošnja_energije(MWh)'].sum()
        trans_pie_2_fig = self.pie(trans_pie_2)
        trans_pie_2_fig.savefig(output_dir / 'potrošnja_energije_transport_gorivo.png', dpi=300, bbox_inches='tight')

        trans_melted['Emisije CO2 (t)'] = trans_melted.apply(
            lambda row: row['potrošnja_energije(MWh)'] * self.co2_factors[row['energent']], axis=1)

        trans_co2_melted = trans_melted.pivot(index='vrsta_prijevoza', columns='energent',
                                              values='Emisije CO2 (t)').fillna(0)
        order = ['Benzin', 'Dizel', 'UNP']
        trans_co2_melted = trans_co2_melted[order]
        trans_co2_melted['Total'] = trans_co2_melted.sum(axis=1)
        trans_co2_melted = trans_co2_melted.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        trans_co2_fig = self.stacked_bar(trans_co2_melted)
        trans_co2_fig.savefig(output_dir / 'transport_co2.png', dpi=300, bbox_inches='tight')

        trans_co2_vrsta_vozila = trans_co2_melted.sum(axis=1)
        trans_co2_vrsta_vozila_fig = self.pie(trans_co2_vrsta_vozila)
        trans_co2_vrsta_vozila_fig.savefig(output_dir / 'transport_co2_vrsta.png', dpi=300, bbox_inches='tight')

        trans_co2_gorivo = trans_co2_melted.sum()
        trans_co2_gorivo_fig = self.pie(trans_co2_gorivo)
        trans_co2_gorivo_fig.savefig(output_dir / 'transport_co2_vrsta.png', dpi=300, bbox_inches='tight')

        """total emissions"""
        ele['energent'] = 'električna energija'

        trans_melted['sektor'] = 'promet'
        ele['sektor'] = 'zgradarstvo'
        heat['sektor'] = 'zgradarstvo'

        columns = ['energent', 'potrošnja_energije(MWh)', 'Emisije CO2 (t)', 'sektor']
        heat = heat[columns]
        ele = ele[columns]
        trans_melted = trans_melted[columns]

        heat = heat.loc[heat['energent'] != 'električna energija']

        total = pd.concat([heat, ele, trans_melted])

        # for 2011
        total.loc[len(total)] = light
        ukupna_potrošnja = total.groupby(['energent', 'sektor'])['potrošnja_energije(MWh)'].sum()
        ukupne_emisije_co2 = total.groupby(['energent', 'sektor'])['Emisije CO2 (t)'].sum()

        total_bar = total.groupby(['sektor', 'energent']).agg({'potrošnja_energije(MWh)': 'sum'}).reset_index()
        total_bar = total_bar.pivot(index='sektor', columns='energent', values='potrošnja_energije(MWh)').fillna(0)
        order = ['električna energija', 'Dizel', 'UNP', 'Benzin', 'lož ulje', 'ogrjevno drvo', 'prirodni plin']
        total_bar = total_bar[order]

        total_fig = self.stacked_bar(total_bar)
        total_fig.savefig(output_dir / 'ukupna_potrošnja.png', dpi=300, bbox_inches='tight')

        total_pie_1 = total.groupby('sektor')['potrošnja_energije(MWh)'].sum()
        total_pie_1_fig = self.pie(total_pie_1)
        total_pie_1_fig.savefig(output_dir / 'ukupna_potrošnja_po_sektoru.png', dpi=300, bbox_inches='tight')

        total_pie_2 = total.groupby('energent')['potrošnja_energije(MWh)'].sum()
        total_pie_2_fig = self.pie(total_pie_2)
        total_pie_2_fig.savefig(output_dir / 'ukupna_potrošnja_po_energentu.png', dpi=300, bbox_inches='tight')

        # co2 chart
        total_co2_bar = total.groupby(['sektor', 'energent']).agg({'Emisije CO2 (t)': 'sum'}).reset_index()
        total_co2_bar = total_co2_bar.pivot(index='sektor', columns='energent', values='Emisije CO2 (t)').fillna(0)
        order = ['električna energija', 'Dizel', 'UNP', 'Benzin', 'lož ulje', 'ogrjevno drvo', 'prirodni plin']
        total_co2_bar = total_co2_bar[order]

        total_co2_fig = self.stacked_bar(total_co2_bar)
        total_co2_fig.savefig(output_dir / 'ukupne_emisije_co2.png', dpi=300, bbox_inches='tight')

        total_co2_pie_1 = total.groupby('sektor')['Emisije CO2 (t)'].sum()
        total_co2_pie_1_fig = self.pie(total_co2_pie_1)
        total_co2_pie_1_fig.savefig(output_dir / 'ukupne_emisije_po_sektoru.png', dpi=300, bbox_inches='tight')

        total_co2_pie_2 = total.groupby('energent')['Emisije CO2 (t)'].sum()
        total_co2_pie_2_fig = self.pie(total_co2_pie_2)
        total_co2_pie_2_fig.savefig(output_dir / 'ukupne_emisije_po_energentu.png', dpi=300, bbox_inches='tight')

        return {
            'heat': heat_pivot,
            'heat_co2': heat_co2_pivot,
            'electricity': ele_bar,
            'electricity_co2': ele_co2_bar,
            'transport': trans_pivot,
            'transport_co2': trans_co2_melted,
            'total': total_bar,
            'total_co2': total_co2_bar,
        }


if __name__ == "__main__":
    constants = Constants()
    # 2011
    output_dir = root_dir / 'output/2011/'
    heat = pd.read_csv(root_dir / 'data/2011/vinkovci_grijanje_2011.csv')
    ele = pd.read_csv(root_dir / 'data/2011/vinkovci_struja_2011.csv')
    trans = pd.read_csv(root_dir / 'data/2011/privatna_vozila_2011.csv')
    light = ['električna energija', 2922.5, 678.0, 'javna rasvjeta']

    #group heat to fit 2019 format
    heat['kategorija'] = heat['kategorija'].replace('objekti i uredi gradskih tvrtki', 'uprava i uredi gradskih tvrtki')
    heat = heat.groupby(['nadkategorija', 'kategorija', 'energent'], as_index=False).sum()

    base_inventory_2011 = Inventory(constants, 2011)
    inventory_2011 = base_inventory_2011.base_inventory(output_dir, heat, ele, trans, light)

    # 2019
    output_dir = root_dir / 'output/2019/'
    heat_2019 = pd.read_csv(root_dir / 'data/2019/vinkovci_grijanje_2019.csv')
    ele_2019 = pd.read_csv(root_dir / 'data/2019/vinkovci_struja_2019.csv')
    trans_2019 = pd.read_csv(root_dir / 'data/2019/privatna_vozila_2019.csv')
    light_2019_mwh = 2008.656
    light_2019_co2 = light_2019_mwh * constants.co2_electricity_mwh_ton_2019
    light_2019 = ['električna energija', light_2019_mwh, light_2019_co2, 'javna rasvjeta']

    base_inventory_2019 = Inventory(constants, 2019)
    inventory_2019 = base_inventory_2019.base_inventory(output_dir, heat_2019, ele_2019, trans_2019, light_2019)

    output_dir = root_dir / 'output/2011v2019/'

    for key in inventory_2019.keys():
        comparison_fig = base_inventory_2019.compare_stacked_bar(
        inventory_2011[key],
        inventory_2019[key],
        '2011',
        '2019'
        )
        comparison_fig.savefig(output_dir / '{}_comparison.png'.format(key), dpi=300, bbox_inches='tight')