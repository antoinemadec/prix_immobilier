#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import numpy as np

l_date = []
l_euros_per_m2 = []

for line in csv.DictReader(open('./35315_000AB.csv', 'r'), delimiter=";"):
    surface = line['surface_reelle_bati']
    price = line['valeur_fonciere']
    date = line['date_mutation']
    rue = line['adresse_nom_voie']
    try:
        surface = int(float(surface))
        price = int(float(price))
    except:
        continue
    if surface < 100 or rue != "RES DES RANSONNIERES":
        continue
    euros_per_m2 = int(price/surface)
    print(f"{date} {price}e {surface}m2 {euros_per_m2}e/m2")
    l_date.append(np.datetime64(date))
    l_euros_per_m2.append(euros_per_m2)

# fig, ax = plt.subplots()
# ax.plot(x, y_est, '-')
# ax.fill_between(x, y_est - y_err, y_est + y_err, alpha=0.2)
# ax.plot(x, y, 'o', color='tab:brown')
# a, b = np.polyfit(x, y, deg=1)

fig, ax = plt.subplots()

ax.plot(l_date, l_euros_per_m2, 'o', color='tab:brown')
plt.show()
