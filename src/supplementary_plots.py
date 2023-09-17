from pathlib import Path

import pandas as pd
import seaborn as sns
import os
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from SupplementaryData import SupplementaryDataConverted


def custom_formatter(x, pos):
    return '{:,.1f}'.format(x).replace(',', ' ').replace('.', ',').replace(' ', '.')



class PlottingUtility:
    def __init__(self):
        sns.set_theme()
        self.colors = sns.color_palette()

    def apply_style(self, ax, y_label, x_label, legend, fix_labels=False):
        SMALL_SIZE = 10
        MEDIUM_SIZE = 14

        plt.rc('font', size=MEDIUM_SIZE)
        plt.rc('axes', titlesize=SMALL_SIZE)
        plt.rc('axes', labelsize=MEDIUM_SIZE)
        plt.rc('xtick', labelsize=MEDIUM_SIZE)
        plt.rc('ytick', labelsize=MEDIUM_SIZE)
        plt.rc('legend', fontsize=MEDIUM_SIZE)

        if fix_labels:
            labels = [' '.join([word.capitalize() for word in label.get_text().split()])
                      if isinstance(label.get_text(), str) else label.get_text() for label in ax.get_yticklabels()]
            ax.set_yticklabels(labels, fontsize=MEDIUM_SIZE)

        else:
            labels = [label.get_text().capitalize() if isinstance(label.get_text(), str) else label.get_text() for label in
                      ax.get_yticklabels()]
            ax.set_yticklabels(labels, fontsize=MEDIUM_SIZE)

        ax.set_xlabel(x_label, fontsize=MEDIUM_SIZE)
        ax.set_ylabel(y_label, fontsize=MEDIUM_SIZE)

        ax.xaxis.set_major_formatter(FuncFormatter(custom_formatter))

        ax.grid(axis='x', linestyle='--', alpha=0.7)

        if not legend:
            ax.legend().set_visible(False)

    def plot_simple_bar(self, data, x_label, y_label, title, legend, output_folder, fix_labels=False):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = [self.colors[5] if idx == "Vukovarsko-srijemska" else self.colors[0] for idx in data.index]
        bars = data.plot(kind='barh', ax=ax, width=0.5, color=colors)
        self.apply_style(ax, x_label, y_label, legend, fix_labels)

        # code for showing values
        for i, (value, index) in enumerate(zip(data.values, data.index)):
            # ax.annotate(str(round(value[0], 2)),
            # (value, i),
            # ha='center',
            # va='center',
            # xytext=(20, 0),  # adjust this value as required
            # textcoords='offset points',
            # fontsize=10)
            if index == "Vukovarsko-srijemska" or index == "Vukovarsko-srijemska županija" or index == "Zelena površina":
                ax.get_yticklabels()[i].set_color(self.colors[2])

        for bar, ytick in zip(ax.containers[0], ax.get_yticklabels()):
            if (ytick.get_text() == "Vukovarsko-srijemska" or ytick.get_text() == "Vukovarsko-srijemska Županija"
                    or ytick.get_text() == "Zelena površina"):
                bar.set_color(self.colors[2])

        plt.savefig(f"{output_folder}/{title}.png", dpi=300, bbox_inches='tight')

    def plot_stacked_bar(self, data, x_label, y_label, title, output_folder, stacked=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='barh', stacked=stacked, ax=ax, width=0.5, color=self.colors)
        legend = ax.legend(fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))
        plt.setp(legend.get_title(), fontsize='small')
        self.apply_style(ax, x_label, y_label, True)
        plt.savefig(f"{output_folder}/{title}.png", dpi=300, bbox_inches='tight')

    def plot_stacked_bar_overlay(self, data, x_label, y_label, title, output_folder):
        fig, ax = plt.subplots(figsize=(10, 6))

        data = data.iloc[::-1]
        col_order = data.sum().sort_values(ascending=False).index

        for index, column in enumerate(col_order):
            if index == 0:
                ax.barh(data.index, data[column], label='Raspoloživi kapacitet', color=self.colors[0], alpha=0.5)
            if index == 1:
                ax.barh(data.index, data[column], label="Zahvaćeni kapacitet 'Sikirevci'", color=self.colors[0], alpha=1)

        legend = ax.legend(fontsize=14, loc='upper left', bbox_to_anchor=(1, 1))
        plt.setp(legend.get_title(), fontsize='small')
        self.apply_style(ax, x_label, y_label, True)
        plt.savefig(f"{output_folder}/{title}.png", dpi=300, bbox_inches='tight')

    def plot_scatter(self, data, x_label, y_label, title, output_folder):
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.lineplot(data=data, x='Mjesec', y='Value', hue='Godina', marker='o', ax=ax)
        ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
        plt.xticks(rotation=45)
        ax.set_xlabel('')
        ax.set_ylabel(y_label)

        plt.savefig(f"{output_folder}/{title}.png", dpi=300, bbox_inches='tight')


def main(output_folder):
    print('Creating supplementary plots')
    if not os.path.exists(output_folder):
        Path(output_folder).mkdir(exist_ok=True, parents=True)

    data = SupplementaryDataConverted()
    plot_util = PlottingUtility()

    plot_util.plot_simple_bar(
        data.land_structure.set_index('Područje').sort_values(by='Value'), "", "Udio (%)",
        "Struktura zemlje", False, output_folder
    )

    plot_util.plot_simple_bar(
        data.land_building_share.set_index('Područje').sort_values(by='Value'), "", "Udio (%)",
        "Struktura građevinskog područja naselja", False, output_folder
    )
    data.water_shortages['sum'] = data.water_shortages['Prosječna godina'] + data.water_shortages['Sušna godina']
    plot_util.plot_stacked_bar(
        data.water_shortages.sort_values(by='sum').drop(columns='sum'), "", "Nedostatak vode (mm)",
        "Nestašice vode", output_folder
    )

    plot_util.plot_simple_bar(
        data.arable_land_structure.set_index('Vrsta građevinskog područja').sort_values(by="Value"), "", "Udio (%)",
        "Struktura poljoprivredne površine", False, output_folder
    )

    plot_util.plot_simple_bar(
        data.arable_land_use.set_index('Vrsta uporabe').sort_values(by='Value'), "",
        "Udio (%)", "Struktura poljoprviredne površine prema vrsti uporabe", False, output_folder
    )

    plot_util.plot_simple_bar(
        data.hummus_per_county.set_index('Županija').sort_values(by='Value'), "", "Zastupljenost (%)",
        "Udio humusa po županiji", False, output_folder
    )

    plot_util.plot_stacked_bar(
        data.agri_employment_age, "", "Udio (%)", 'Godište zaposlenih u poljoprivredi',
        output_folder, False
    )

    plot_util.plot_simple_bar(
        data.employment_vinkovci.set_index('Employment Type').sort_values(by='Value'), "",
        "Udio (%)", "Zaposleni po industriji", False, output_folder
    )

    plot_util.plot_simple_bar(
        data.bdp_index_region.set_index('Region').sort_values(by='Value'), "",
        "Indeks po glavi stanovnika", "BDP indeks po regiji", False, output_folder, True
    )

    plot_util.plot_stacked_bar(
        data.agri_education, "", "Udio (%)", "Obrazovanje u poljoprivredi", output_folder, False
    )
    data.turism_seasonality = data.turism_seasonality.rename(columns={
        0: '2019.',
        1: '2020.',
        2: '2021.',
        3: '2022.'
    })
    data.turism_seasonality = data.turism_seasonality.reset_index().melt(
        id_vars="index", value_vars=data.turism_seasonality.columns
    )
    data.turism_seasonality.columns = ['Mjesec', 'Godina', 'Value']
    plot_util.plot_scatter(
        data.turism_seasonality, "", "Broj dolazaka", "Sezonalnost turizma", output_folder
    )

    data.precipitation = data.precipitation.rename(columns={
        0: '2019.',
        1: '2020.',
        2: '2021.',
        3: '2022.'
    })

    data.precipitation = data.precipitation.reset_index().melt(
        id_vars="index", value_vars=data.precipitation.columns
    )
    data.precipitation.columns = ['Mjesec', 'Godina', 'Value']
    plot_util.plot_scatter(
        data.precipitation, "", "Količina oborina (mm)", "Godišnja količina oborina", output_folder
    )

    plot_util.plot_stacked_bar(
        data.arrivals_sleepovers, "", "Broj",
        "Broj dolazaka i broj noćenja", output_folder, False
    )

    plot_util.plot_simple_bar(
        data.employment_tourism.set_index('Year'), "", "Udio zaposlenih u turizmu (%)",
        "Udio zaposlenih u turizmu", False, output_folder
    )

    plot_util.plot_stacked_bar(
        data.tourists_per_capita, "", "Broj po glavi stanovnika",
        "Broj turista i noćenja per capita", output_folder, False
    )

    plot_util.plot_simple_bar(
        data.water_requirements.set_index('Month').iloc[::-1], "", "Zahvat količine vode (m3)",
        "Potreba za vodom 2021", False, output_folder
    )

    plot_util.plot_stacked_bar(
        data.damages_plumbing, "", "Broj kvarova",
        "Broj kvarova po godinama", output_folder, True
    )

    plot_util.plot_simple_bar(
        data.water_loss.set_index('Year'), "", "Udio gubitaka u vodoopskrbi (%)",
        "Gubici vode po godinama", False, output_folder
    )

    data.water_capacity.columns = ["Zahvaćeni kapacitet vode 'Sikirevci'", 'Raspoloživi kapacitet']
    plot_util.plot_stacked_bar_overlay(
        data.water_capacity, "", "Kapacitet (l/s)", "Raspoloživi kapacitet vode", output_folder
    )

    data.water_samples.columns = [
        'Uzorci fiz.-kem.',
        'Neuskladni uzorci fiz.-kem.',
        'Uzorci mikrobiološki',
        'Neuskladni uzorci mikrobiološki'
    ]
    plot_util.plot_stacked_bar(
        data.water_samples, "", "Broj uzoraka", "Analize uzoraka vode", output_folder, False
    )

    plot_util.plot_simple_bar(
        data.use_of_land.set_index('Namjena površine').sort_values(by='Value'), "",
        "Udio (%)", "Namjena površine", False, output_folder
    )

    print('Finished creating supplementary plots')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate plots for the provided datasets.')
    parser.add_argument('-o', '--output_folder', type=str, required=True,
                        help='Path to the output folder where plots will be saved.')
    args = parser.parse_args()
    main(args.output_folder)
