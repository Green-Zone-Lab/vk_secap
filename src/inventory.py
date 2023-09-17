import matplotlib
import numpy as np
import seaborn as sns
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from numpy.polynomial import Polynomial

from .Constants import Constants

root_dir = Path(__file__).parents[1]

def custom_formatter(x, pos):
    return '{:,.1f}'.format(x).replace(',', ' ').replace('.', ',').replace(' ', '.')

def adjust_label_distance(texts, autotexts):
    for i, text in enumerate(texts):
        if text.get_text() in ["Autobusni"]:
            text.set_position((1.15 * text.get_position()[0], 1.15 * text.get_position()[1]))
            autotexts[i].set_position((1.15 * autotexts[i].get_position()[0], 1.15 * autotexts[i].get_position()[1]))


def comma_decimal(x, _):
    return "{:.2f}".format(x).replace('.', ',')


def comma_decimal_percent(pct, allvals):
    absolute = int(round(pct / 100. * np.sum(allvals)))
    if absolute == 0:
        return ""
    return "{:.1f}%".format(pct, absolute)


def percent_difference(df1, df2):
    percent_diff = ((df2 - df1) / df1) * 100
    return percent_diff


def electricity_emission_factor_2030():
    sns.set_theme()
    sns.set_style()
    SMALL_SIZE = 10
    MEDIUM_SIZE = 14

    color_palette = sns.color_palette()

    fig, ax = plt.subplots(figsize=(10, 6))

    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize

    file_path = Path(root_dir / "data" / "public_data/JRC-COM-NEEFE_1990-2020.xlsx")
    df = pd.read_excel(file_path, sheet_name=1, skiprows=1, engine='openpyxl')
    emission_factors = df.loc[df['Unnamed: 0'] == 'Croatia'].drop(columns='Unnamed: 0').melt()
    x = emission_factors['variable'].values.astype(int)
    y = emission_factors['value'].values.astype(float)

    p = Polynomial.fit(x, y, 3)
    predicted_2030 = p(2030)

    x_dense = np.linspace(min(x), 2030, 400)
    y_dense = p(x_dense)

    sns.scatterplot(x=x, y=y, ax=ax, color='blue')
    ax.plot(x_dense, y_dense, color='red')
    ax.scatter(2030, predicted_2030, color='green', marker='x', s=100, label='Predviđanje za 2030')
    ax.annotate(f'{predicted_2030:.3f}', (2030, predicted_2030), textcoords="offset points", xytext=(0, 10),
                ha='center')

    # Set x and y labels
    ax.set_xlabel('Godina')
    ax.set_ylabel('Emisijske faktor kg(CO2)/kWh')

    ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))

    return predicted_2030, fig



class Inventory:
    def __init__(self, constants, year):
        color_palette = sns.color_palette()

        pd.set_option('display.float_format', lambda x: '%.1f' % x)
        self.constants = constants

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
            'lož ulje': color_palette[1],
            'električna energija': color_palette[0],
            'prirodni plin': color_palette[3],
            'ogrjevno drvo': color_palette[5],
            'Dizel': color_palette[8],
            'Benzin': color_palette[9],
            'UNP': color_palette[6],

            'stambeni objekti': color_palette[0],
            'zgrade komercijalnog i uslužnog karaktera': color_palette[1],
            'zgrade javne namjene': color_palette[2],

            'teretna i radna vozila': color_palette[6],
            'osobna vozila': color_palette[7],
            'ostalo': color_palette[8],
            'autobusni': color_palette[9],
            'mopedi i motocikli': color_palette[4],

        }

    def stacked_bar(self, data, title):
        sns.set_theme()
        sns.set_style()
        SMALL_SIZE = 10
        MEDIUM_SIZE = 14

        plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize

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
        legend = None
        try:
            colors = [self.colors[energent] for energent in data.columns]
            data.plot(kind='barh', stacked=True, ax=ax, width=0.5, color=colors)
            legend = ax.legend(fontsize=MEDIUM_SIZE, loc='upper left', bbox_to_anchor=(1, 1))
            plt.setp(legend.get_title(), fontsize='small')
        except AttributeError:
            data.plot(kind='barh', stacked=False, ax=ax, width=0.5)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        labels = [label.get_text().capitalize() if isinstance(label.get_text(), str) else label.get_text() for label
                  in ax.get_yticklabels()]
        ax.set_yticklabels(labels, fontsize=MEDIUM_SIZE)

        if legend:  # Check if a legend exists
            for text in legend.get_texts():
                text.set_text(text.get_text().capitalize())

        ax.set_xlabel(title, fontsize=MEDIUM_SIZE)
        ax.set_ylabel("")

        # if log:
        # ax.set_xscale('log')

        return fig

    def compare_stacked_bar(self, data1, data2, year1, year2, title):
        sns.set_theme()
        sns.set_style()
        SMALL_SIZE = 10
        MEDIUM_SIZE = 14

        color_palette = sns.color_palette()

        plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize

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

        # Merge the two dataframes side by side
        merged_data = pd.concat([data1, data2], axis=1, keys=['Year1', 'Year2'])

        # Get the colors for each energent
        legend = None
        try:
            colors1 = [self.colors[energent] for energent in data1.columns]
            colors2 = [self.colors[energent] for energent in data2.columns]

            # Plot the first year's data with slightly reduced alpha for distinction
            merged_data['Year1'].plot(kind='barh', stacked=True, ax=ax, width=0.3, color=colors1, position=0, alpha=0.6,
                                      label=[f"{year1} - {col}" for col in data1.columns])

            # Plot the second year's data
            merged_data['Year2'].plot(kind='barh', stacked=True, ax=ax, width=0.3, color=colors2, position=1, alpha=1,
                                      label=[f"{year2} - {col}" for col in data2.columns])
            legend_labels = [f"{year1} - {col}" for col in data1.columns] + [f"{year2} - {col}" for col in
                                                                             data2.columns]
            handles, _ = ax.get_legend_handles_labels()
            legend = ax.legend(handles[:len(legend_labels)], legend_labels, fontsize=MEDIUM_SIZE, loc='upper left',
                               bbox_to_anchor=(1, 1))

        except AttributeError:
            merged_data['Year1'].plot(kind='barh', stacked=False, ax=ax, width=0.3, position=0, alpha=0.6,
                                      label=f"{year1}")
            merged_data['Year2'].plot(kind='barh', stacked=False, ax=ax, width=0.3, position=1, alpha=1,
                                      label=f"{year2}")

        ax.grid(axis='x', linestyle='--', alpha=0.7)

        labels = [label.get_text().capitalize() if isinstance(label.get_text(), str) else label.get_text() for label
                  in ax.get_yticklabels()]
        ax.set_yticklabels(labels, fontsize=MEDIUM_SIZE)

        ax.set_xlabel(title, fontsize=MEDIUM_SIZE)
        ax.set_ylabel("")

        year_legend_y_position = 1
        try:
            unique_labels = {}
            for energent in data1.columns:
                unique_labels[energent] = self.colors[energent]
            for energent in data2.columns:
                unique_labels[energent] = self.colors[energent]

            energy_patches = [matplotlib.patches.Patch(color=color, label=label.capitalize()) for label, color in
                              unique_labels.items()]

            legend_energy = ax.legend(handles=energy_patches, fontsize=MEDIUM_SIZE, loc='upper left',
                                      bbox_to_anchor=(1, 1))
            legend_energy_height_per_item = 0.05  # this is an estimated height per item
            total_height = legend_energy_height_per_item * len(energy_patches)
            year_legend_y_position = 1 - total_height - 0.1  # little gap
            plt.gca().add_artist(legend_energy)
        except:
            print('Input is a series')

        year_patches = [matplotlib.patches.Patch(color=color_palette[0], alpha=0.4, label=str(year1)),
                        matplotlib.patches.Patch(color=color_palette[0], alpha=1, label=str(year2))]

        ax.legend(handles=year_patches, fontsize=MEDIUM_SIZE, loc='upper left',
                  bbox_to_anchor=(1, year_legend_y_position))

        # if log:
        #     ax.set_xscale('log')

        return fig

    def projection_bar(self, data, title):
        # Styling and fonts settings as provided
        sns.set_theme()
        sns.set_style("whitegrid")
        SMALL_SIZE = 10
        MEDIUM_SIZE = 14
        plt.rc('font', size=MEDIUM_SIZE)
        plt.rc('axes', titlesize=SMALL_SIZE)
        plt.rc('axes', labelsize=MEDIUM_SIZE)
        plt.rc('xtick', labelsize=MEDIUM_SIZE)
        plt.rc('ytick', labelsize=MEDIUM_SIZE)
        plt.rc('legend', fontsize=MEDIUM_SIZE)

        # Colors
        color_palette = sns.color_palette()
        colors = {
            'javna rasvjeta': color_palette[0],
            'promet': color_palette[1],
            'zgradarstvo': color_palette[2],
        }

        data_pivot = data.pivot(index='Godina', columns='sektor', values=0)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = data_pivot.plot(kind='bar', stacked=True, ax=ax, width=0.3,
                               color=[colors[col] for col in data_pivot.columns])

        heights = []
        for bar in bars.patches:
            heights.append(bar.get_y() + bar.get_height() / 2)

        # Calculate the total heights of the bars for 2019 and 2030
        total_height_2019 = data[data['Godina'] == 2019][0].sum()
        total_height_2030 = data[data['Godina'] == 2030][0].sum()

        # Drawing the horizontal lines
        ax.axhline(y=total_height_2019, xmin=0.305, xmax=0.86, color='green', linestyle='--')
        ax.axhline(y=total_height_2030, xmin=0.305, xmax=0.86, color='green', linestyle='--')

        # Calculating the percentage change
        if total_height_2019 != 0:
            percent_change = ((total_height_2030 - total_height_2019) / total_height_2019) * 100
        else:
            percent_change = 100  # if the 2019 bar's height is 0, then it's a full increase, so consider it 100%

        diff_position = (total_height_2030 + total_height_2019) / 2
        ax.text(1 / 2, diff_position + abs(total_height_2030 - total_height_2019) / 20, f'{percent_change:.2f}%',
                horizontalalignment='center', verticalalignment='center', fontsize=14, color='green')

        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_ylabel(title)

        legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        if legend:  # Check if a legend exists
            for text in legend.get_texts():
                text.set_text(text.get_text().capitalize())

        return fig

    def pie(self, data):
        sns.set_theme()
        sns.set_style()
        SMALL_SIZE = 10
        MEDIUM_SIZE = 14

        plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
        color_palette = sns.color_palette()

        self.colors = {
            # fuels
            'Lož ulje': color_palette[1],  # 'orange'
            'Električna energija': color_palette[0],  # 'blue'
            'Prirodni plin': color_palette[3],  # 'red'
            'Ogrjevno drvo': color_palette[5],  # 'green'
            'Dizel': color_palette[8],
            'Benzin': color_palette[9],
            'Unp': color_palette[6],

            # buildings
            'Stambeni objekti': color_palette[0],  # 'blue'
            'Zgrade komercijalnog i uslužnog karaktera': color_palette[1],  # 'orange',
            'Zgrade javne namjene': color_palette[2],  # 'green'

            # transport
            'Teretna i radna vozila': color_palette[6],
            'Osobna vozila': color_palette[7],
            'Ostalo': color_palette[8],
            'Autobusni': color_palette[9],
            'Mopedi i motocikli': color_palette[4],

            # sectors
            'Javna rasvjeta': color_palette[5],  # 'red
            'Zgradarstvo': color_palette[7],
            'Promet': color_palette[0],

        }

        fig, ax = plt.subplots(figsize=(10, 6))
        data.index = data.index.str.capitalize()
        patches, texts, autotexts = ax.pie(
            data.values,
            labels=data.index.str.capitalize(),
            autopct=lambda pct: comma_decimal_percent(pct, data.values),
            startangle=90,
            colors=[self.colors[energent] for energent in data.index]
        )

        adjust_label_distance(texts, autotexts)

        ax.set_ylabel('')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(comma_decimal))

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

        heat_by_sector = self.stacked_bar(heat_pivot, title='Potrošnja energije (MWh)')
        heat_by_sector.savefig(output_dir / 'potrošnja_toplinske.png', dpi=300, bbox_inches='tight')

        # stacked bar for heat CO2 by sector and fuel
        heat_co2_pivot = heat.pivot(index='kategorija', columns='energent', values='Emisije CO2 (t)').fillna(0)
        order = ['prirodni plin', 'lož ulje', 'ogrjevno drvo', 'električna energija']
        heat_co2_pivot = heat_co2_pivot[order]
        heat_co2_pivot['Total'] = heat_co2_pivot.sum(axis=1)
        heat_co2_pivot = heat_co2_pivot.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        heat_co2_by_sector = heat_co2_pivot.drop(columns=['ogrjevno drvo'])
        heat_co2_by_sector = self.stacked_bar(heat_co2_by_sector, title='Emisije CO2 (t)')
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
        ele_bar_fig = self.stacked_bar(ele_bar, title='Potrošnja energije (MWh)')
        ele_bar_fig.savefig(output_dir / 'potrošnja_električne.png', dpi=300, bbox_inches='tight')

        # electricity co2 emissions
        ele_co2_bar = ele.groupby('kategorija')['Emisije CO2 (t)'].sum()
        ele_co2_bar = ele_co2_bar.sort_values(ascending=True)
        ele_co2_bar_fig = self.stacked_bar(ele_co2_bar, title='Emisije CO2 (t)')
        ele_co2_bar_fig.savefig(output_dir / 'emisije_co2_električne.png', dpi=300, bbox_inches='tight')

        # pie charts

        ele_pie_1 = ele.groupby('nadkategorija')['potrošnja_energije(MWh)'].sum()
        if 'ostalo' in ele_pie_1.index:
            ele_pie_1 = ele_pie_1.drop('ostalo')
        ele_pie_1_fig = self.pie(ele_pie_1)
        ele_pie_1_fig.savefig(output_dir / 'potrošnja_električne_sektor.png', dpi=300, bbox_inches='tight')

        ele_co2_pie_1 = ele.groupby('nadkategorija')['Emisije CO2 (t)'].sum()
        if 'ostalo' in ele_co2_pie_1.index:
            ele_co2_pie_1 = ele_co2_pie_1.drop('ostalo')
        ele_co2_pie_1_fig = self.pie(ele_co2_pie_1)
        ele_co2_pie_1_fig.savefig(output_dir / 'emisije_co2_električne_sektor.png', dpi=300, bbox_inches='tight')

        """transport data"""
        trans = trans.loc[trans['vrsta_prijevoza'] != 'taxi']
        trans = trans.fillna(0)
        trans['Dizel'] = trans['procijenjena_potrošena_masa_dizela(t)'] * self.constants.diesel_ton_mwh
        trans['Benzin'] = trans['procijenjena_potrošena_masa_benzina(t)'] * self.constants.petrol_ton_mwh
        trans['UNP'] = trans['procijenjena_potrošena_masa_unp(t)'] * self.constants.lpg_ton_mwh

        order = ['Dizel', 'Benzin', 'UNP']
        trans_pivot = trans.set_index('vrsta_prijevoza')
        trans_pivot = trans_pivot[order]
        trans_pivot['Total'] = trans_pivot.sum(axis=1)
        trans_pivot = trans_pivot.sort_values(by='Total', ascending=True).drop(columns=['Total'])

        trans_pivot_fig = self.stacked_bar(trans_pivot, title='Potrošnja energije (MWh)')
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

        trans_co2_fig = self.stacked_bar(trans_co2_melted, title='Emisije CO2 (t)')
        trans_co2_fig.savefig(output_dir / 'transport_co2.png', dpi=300, bbox_inches='tight')

        trans_co2_vrsta_vozila = trans_co2_melted.sum(axis=1)
        trans_co2_vrsta_vozila_fig = self.pie(trans_co2_vrsta_vozila)
        trans_co2_vrsta_vozila_fig.savefig(output_dir / 'transport_co2_vrsta.png', dpi=300, bbox_inches='tight')

        trans_co2_gorivo = trans_co2_melted.sum()
        trans_co2_gorivo_fig = self.pie(trans_co2_gorivo)
        trans_co2_gorivo_fig.savefig(output_dir / 'transport_co2_gorivo.png', dpi=300, bbox_inches='tight')

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

        total_fig = self.stacked_bar(total_bar, title='Potrošnja energije (MWh)')
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
        order = ['električna energija', 'Dizel', 'UNP', 'Benzin', 'lož ulje', 'prirodni plin']
        total_co2_bar = total_co2_bar[order]

        total_co2_fig = self.stacked_bar(total_co2_bar, title='Emisije CO2 (t)')
        total_co2_fig.savefig(output_dir / 'ukupne_emisije_co2.png', dpi=300, bbox_inches='tight')

        total_co2_pie_1 = total.groupby('sektor')['Emisije CO2 (t)'].sum()
        total_co2_pie_1_fig = self.pie(total_co2_pie_1)
        total_co2_pie_1_fig.savefig(output_dir / 'ukupne_emisije_po_sektoru.png', dpi=300, bbox_inches='tight')

        total_co2_pie_2 = total.groupby('energent')['Emisije CO2 (t)'].sum()
        total_co2_pie_2 = total_co2_pie_2.drop('ogrjevno drvo')
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

    # fuel consumption is 2011 is too low, adjust to the same calculation as in 2019
    km_per_vehicle = 12542  # same km per year per vehicle
    factor = constants.specific_consumption_petrol_2000 / constants.specific_consumption_diesel_2000  # how much more petrol is spent
    # adjust the fuel to get proportions
    petrol_adj = trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila'][
                     'procijenjena_potrošena_masa_benzina(t)'] / factor
    lpg_adj = trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila']['procijenjena_potrošena_masa_unp(t)'] / factor
    diesel_adj = trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila']['procijenjena_potrošena_masa_dizela(t)']
    total = petrol_adj + lpg_adj + diesel_adj

    prop_petrol = petrol_adj / total
    prop_lpg = lpg_adj / total
    prop_diesel = diesel_adj / total

    # calculate tons of fuel
    diesel_spent = prop_diesel * trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila'][
        'broj'] * constants.diesel_km_per_year * constants.specific_consumption_diesel_2000 * constants.diesel_litre_to_ton
    petrol_spent = prop_petrol * trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila'][
        'broj'] * constants.petrol_km_per_year * constants.specific_consumption_petrol_2000 * constants.petrol_litre_to_ton
    lpg_spent = prop_lpg * trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila'][
        'broj'] * constants.unp_km_per_year * constants.specific_consumption_petrol_2000 * constants.lpg_petrol_index * constants.lpg_litre_to_ton

    # fix values for cars
    trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila', 'procijenjena_potrošena_masa_benzina(t)'] = petrol_spent
    trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila', 'procijenjena_potrošena_masa_dizela(t)'] = diesel_spent
    trans.loc[trans['vrsta_prijevoza'] == 'osobna vozila', 'procijenjena_potrošena_masa_unp(t)'] = lpg_spent

    # fix values for trucks
    petrol_adj = trans.loc[trans['vrsta_prijevoza'] == 'teretna i radna vozila'][
                     'procijenjena_potrošena_masa_benzina(t)'] / factor
    diesel_adj = trans.loc[trans['vrsta_prijevoza'] == 'teretna i radna vozila'][
        'procijenjena_potrošena_masa_dizela(t)']
    total = petrol_adj + diesel_adj

    prop_petrol = petrol_adj / total
    prop_diesel = diesel_adj / total

    diesel_spent = prop_diesel * trans.loc[trans['vrsta_prijevoza'] == 'teretna i radna vozila'][
        'broj'] * constants.heavy_km_per_year * constants.specific_consumption_diesel_2000 * constants.diesel_litre_to_ton
    petrol_spent = prop_petrol * trans.loc[trans['vrsta_prijevoza'] == 'teretna i radna vozila'][
        'broj'] * constants.heavy_km_per_year * constants.specific_consumption_petrol_2000 * constants.petrol_litre_to_ton

    trans.loc[
        trans['vrsta_prijevoza'] == 'teretna i radna vozila', 'procijenjena_potrošena_masa_benzina(t)'] = petrol_spent
    trans.loc[
        trans['vrsta_prijevoza'] == 'teretna i radna vozila', 'procijenjena_potrošena_masa_dizela(t)'] = diesel_spent

    # fix values for bikes
    petrol_spent = trans.loc[trans['vrsta_prijevoza'] == 'mopedi i motocikli'][
                       'broj'] * constants.bikes_km_per_year * constants.specific_consumption_petrol_2000 * constants.petrol_litre_to_ton
    trans.loc[
        trans['vrsta_prijevoza'] == 'mopedi i motocikli', 'procijenjena_potrošena_masa_benzina(t)'] = petrol_spent

    # group heat to fit 2019 format
    heat['kategorija'] = heat['kategorija'].replace('objekti i uredi gradskih tvrtki', 'uprava i uredi gradskih tvrtki')
    heat['kategorija'] = heat['kategorija'].replace('uprava', 'uprava i uredi gradskih tvrtki')
    heat = heat.groupby(['nadkategorija', 'kategorija', 'energent'], as_index=False).sum()

    # group electricity to fit 2019 format
    ele['kategorija'] = ele['kategorija'].replace('objekti i uredi gradskih tvrtki', 'uprava i uredi gradskih tvrtki')
    ele['kategorija'] = ele['kategorija'].replace('uprava', 'uprava i uredi gradskih tvrtki')
    ele = ele.groupby(['nadkategorija', 'kategorija'], as_index=False).sum()

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

    # 2011 vs 2019
    output_dir = root_dir / 'output/2011v2019/'
    co2_keys = [key for key in inventory_2019.keys() if key.endswith('co2')]
    mwh_keys = [key for key in inventory_2019.keys() if not key.endswith('co2')]
    for key in co2_keys:
        comparison_fig = base_inventory_2019.compare_stacked_bar(
            inventory_2011[key],
            inventory_2019[key],
            '2011',
            '2019',
            'Emisije CO2 (t)',
        )
        comparison_fig.savefig(output_dir / '{}_comparison.png'.format(key), dpi=300, bbox_inches='tight')

    for key in mwh_keys:
        comparison_fig = base_inventory_2019.compare_stacked_bar(
            inventory_2011[key],
            inventory_2019[key],
            '2011',
            '2019',
            'Potrošnja energije (MWh)',
        )
        comparison_fig.savefig(output_dir / '{}_comparison.png'.format(key), dpi=300, bbox_inches='tight')

    """ create supplementary output dir """
    supplementary_output = root_dir / 'output_supplementary/'

    """ mitigation measures effect business as usual"""
    # electricity 2030 emission index
    ele_2030_index, ele_figure = electricity_emission_factor_2030()
    ele_figure.savefig(supplementary_output / 'electricity_2030_emission_factor', dpi=300, bbox_inches='tight')

    # business as usual scenario
    change_per_year = percent_difference(
        inventory_2011['total'].sum(axis=1),
        inventory_2019['total'].sum(axis=1)
    ) / 8

    change_until_2030 = change_per_year * 11 / 100
    change_inventory_2030 = inventory_2019['total'].sum(axis=1) * change_until_2030
    inventory_2030 = inventory_2019['total'].sum(axis=1) + change_inventory_2030

    # use 0.025 share of electric cars from Offical strategy (NN 25/2020)
    n_electric_cars_2030 = int(trans_2019.sum()['broj'] - (trans_2019.sum()['broj'] * 0.025))

    # approximate as energy consumption per car
    energy_per_car = inventory_2019['total'].sum(axis=1)['promet'] / trans_2019.sum()['broj']
    energy_trans_2030 = energy_per_car * n_electric_cars_2030
    inventory_2030['promet'] = energy_trans_2030

    # co2 change to 2030
    electricity_co2_2019 = inventory_2019['total_co2']['električna energija'].sum()
    dif_ele_emission_factor = ele_2030_index / constants.co2_electricity_mwh_ton_2019
    electricity_co2_2030_saved_light = (1 - dif_ele_emission_factor) * \
                                       inventory_2019['total_co2'].loc['javna rasvjeta']['električna energija']
    electricity_co2_2030_saved_buildings = (1 - dif_ele_emission_factor) * \
                                           inventory_2019['total_co2'].loc['zgradarstvo']['električna energija']

    inventory_2030_co2 = inventory_2019['total_co2'].copy()
    inventory_2030_co2.loc['javna rasvjeta']['električna energija'] = inventory_2030_co2.loc['javna rasvjeta'][
                                                                          'električna energija'] - electricity_co2_2030_saved_light
    inventory_2030_co2.loc['zgradarstvo']['električna energija'] = inventory_2030_co2.loc['zgradarstvo'][
                                                                       'električna energija'] - electricity_co2_2030_saved_buildings
    co2_2030_sector_scaling = inventory_2030_co2.sum(axis=1) / inventory_2019['total'].sum(axis=1)
    inventory_2030_co2 = inventory_2030 * co2_2030_sector_scaling

    # format data for projection chart
    inventory_2030 = inventory_2030.reset_index()
    inventory_2019_total = inventory_2019['total'].sum(axis=1).reset_index()
    inventory_2019_total['Godina'] = 2019
    inventory_2030['Godina'] = 2030
    projection_total = pd.concat([inventory_2019_total, inventory_2030])
    energy_projection_2030 = base_inventory_2019.projection_bar(projection_total, 'Potrošnja energije (MWh)')
    energy_projection_2030.savefig(
        supplementary_output / 'energy_2030_projection_as_usual.ong', dpi=300, bbox_inches='tight'
    )

    inventory_2030_co2 = inventory_2030_co2.reset_index()
    inventory_2019_total_co2 = inventory_2019['total_co2'].sum(axis=1).reset_index()
    inventory_2019_total_co2['Godina'] = 2019
    inventory_2030_co2['Godina'] = 2030
    projection_total = pd.concat([inventory_2019_total_co2, inventory_2030_co2])
    co2_projection_2030 = base_inventory_2019.projection_bar(projection_total, 'Emisije CO2 (t)')
    co2_projection_2030.savefig(
        supplementary_output / 'co2_2030_projection_as_usual.ong', dpi=300, bbox_inches='tight'
    )

    # co2 scenario COM - share of electric cars S1 - "Scenarij ubrzane energetske tranzicije"
    # savings of 7.5% total energy and CO2 for eco-driving
    # savings of 5% total energy and CO2 for bikes
    eco_driving = inventory_2019['total'].sum(axis=1)['promet'] * 0.075
    bike_mobility = inventory_2019['total'].sum(axis=1)['promet'] * 0.05

    eco_driving_co2 = inventory_2019['total_co2'].sum(axis=1)['promet'] * 0.075
    bike_mobility_co2 = inventory_2019['total_co2'].sum(axis=1)['promet'] * 0.05

    n_electric_cars_2030_s2 = int(trans_2019.sum()['broj'] - (trans_2019.sum()['broj'] * 0.045))
    energy_per_car_s2 = inventory_2019['total'].sum(axis=1)['promet'] / trans_2019.sum()['broj']
    energy_trans_2030_s2 = energy_per_car_s2 * n_electric_cars_2030_s2

    inventory_2030_s2 = inventory_2030.copy()
    inventory_2030_s2.loc[inventory_2030_s2['sektor'] == 'promet', 0] = energy_trans_2030_s2

    promet_loc = inventory_2030_s2['sektor'] == 'promet'
    inventory_2030_s2.loc[promet_loc, 0] = inventory_2030_s2.loc[promet_loc][0] - eco_driving
    inventory_2030_s2.loc[promet_loc, 0] = inventory_2030_s2.loc[promet_loc][0] - bike_mobility_co2
    inventory_2030_s2.loc[promet_loc, 0] = inventory_2030_s2.loc[promet_loc][0] - 2398.9

    inventory_2030_s2 = inventory_2030.copy()
    inventory_2030_s2.loc[inventory_2030_s2['sektor'] == 'promet', 0] = energy_trans_2030_s2

    zgradarstvo_loc = inventory_2030_s2['sektor'] == 'zgradarstvo'
    inventory_2030_s2.loc[zgradarstvo_loc, 0] = inventory_2030_s2.loc[zgradarstvo_loc][0] - 71899.84

    rasvjeta_loc = inventory_2030_s2['sektor'] == 'javna rasvjeta'
    inventory_2030_s2.loc[rasvjeta_loc, 0] = inventory_2030_s2.loc[rasvjeta_loc][0] - 365.568
    promet_loc = inventory_2030_s2['sektor'] == 'promet'

    projection_total = pd.concat([inventory_2019_total, inventory_2030_s2])
    projection_s2 = base_inventory_2019.projection_bar(projection_total, 'Potrošnja energije (MWh)')
    projection_s2.savefig(
        supplementary_output / 'energy_2030_projection_COM.png', dpi=300, bbox_inches='tight'
    )

    # Co2 projection
    inventory_2030_co2_s2 = inventory_2030_co2.copy()
    ele_car_savings = inventory_2030_co2_s2.loc[inventory_2030_co2_s2['sektor'] == 'promet'][0] * 0.02
    promet_loc_co2 = inventory_2030_co2_s2['sektor'] == 'promet'
    inventory_2030_co2_s2.loc[promet_loc_co2, 0] = (inventory_2030_co2_s2.loc[promet_loc_co2][0]
                                                    - ele_car_savings - eco_driving_co2 - bike_mobility_co2 - 566.21)
    zgradarstvo_loc_co2 = inventory_2030_co2_s2['sektor'] == 'zgradarstvo'
    inventory_2030_co2_s2.loc[zgradarstvo_loc_co2, 0] = inventory_2030_co2_s2.loc[zgradarstvo_loc_co2][0] - 14654.86

    projection_total = pd.concat([inventory_2019_total_co2, inventory_2030_co2_s2])
    projection_co2_s2 = base_inventory_2019.projection_bar(projection_total, 'Emisije CO2 (t)')
    projection_co2_s2.savefig(
        supplementary_output / 'co2_2030_projection_COM.png', dpi=300, bbox_inches='tight'
    )


