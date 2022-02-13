#!/usr/bin/env python3

import argparse
import csv
import datetime as DT

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

# arg parsing
parser = argparse.ArgumentParser(description='plot euros/m2 from csv')
parser.add_argument('csv_files', nargs='+', help='csv files from https://app.dvf.etalab.gouv.fr/')
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
        try:
            surface = int(float(surface))
            price = int(float(price))
        except:
            continue
        # if surface < 100 or surface > 200 or rue != "RES DES RANSONNIERES":
        if surface < 130 or surface > 200:
            continue
        euros_per_m2 = int(price/surface)
        print(f"{date} {price}e {surface}m2 {euros_per_m2}e/m2")
        date_args = [int(s) for s in date.split('-')]
        l_date.append(DT.datetime(date_args[0], date_args[1], date_args[2]))
        l_euros_per_m2.append(euros_per_m2)

fig, ax = plt.subplots()
ax.plot(l_date, l_euros_per_m2, 'o', color='tab:brown')

# estimate
dates = l_date
y = l_euros_per_m2
x = mdates.date2num(dates)
z4 = np.polyfit(x, y, 2)
p4 = np.poly1d(z4)
xx = np.linspace(x.min(), x.max(), 100)
dd = mdates.num2date(xx)
ax.plot(dd, p4(xx), '-g')
ax.plot(dates, y, '+', color='b', label='blub')

# show
ax.grid()
plt.show()
