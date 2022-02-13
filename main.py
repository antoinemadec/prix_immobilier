#!/usr/bin/env python3

import argparse
import csv
import datetime as DT

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def plot_estimate(dates, y, deg, ax, color="blue"):
    x = mdates.date2num(dates)
    z4 = np.polyfit(x, y, deg)
    p4 = np.poly1d(z4)
    xx = np.linspace(x.min(), mdates.date2num(DT.date.today()), 100)
    dd = mdates.num2date(xx)
    ax.plot(dd, p4(xx), color=color)


# arg parsing
parser = argparse.ArgumentParser(description='plot euros/m2 from csv')
parser.add_argument('csv_files', nargs='+',
                    help='csv files from https://app.dvf.etalab.gouv.fr/')
args = parser.parse_args()

# actual data
l_date = []
l_euros_per_m2 = []
for filepath in args.csv_files:
    for line in csv.DictReader(open(filepath, 'r'), delimiter=";"):
        surface = line['surface_reelle_bati']
        price = line['valeur_fonciere']
        date = line['date_mutation']
        rue = line['adresse_nom_voie']
        type = line['type_local']
        try:
            surface = int(float(surface))
            price = int(float(price))
        except:
            continue
        # or rue != "RES DES RANSONNIERES":
        if type != "Maison":
            continue
        euros_per_m2 = int(price/surface)
        print(f"{date} {price}e {surface}m2 {euros_per_m2}e/m2")
        date_args = [int(s) for s in date.split('-')]
        l_date.append(DT.datetime(date_args[0], date_args[1], date_args[2]))
        l_euros_per_m2.append(euros_per_m2)

fig, ax = plt.subplots()
ax.plot(l_date, l_euros_per_m2, '+', color='orange')

# estimate
plot_estimate(l_date, l_euros_per_m2, 1, ax, color="lightblue")
plot_estimate(l_date, l_euros_per_m2, 2, ax, color="blue")
plot_estimate(l_date, l_euros_per_m2, 3, ax, color="darkblue")

# show
ax.grid()
plt.show()
