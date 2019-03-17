import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import collections

from scipy.spatial.distance import pdist, squareform
from scipy import mean


def srednia(lista):
    dlugosc = len(lista)
    suma = 0
    for i in range(dlugosc):
        suma += lista[i]
    return suma/dlugosc


xys = []

with open('objects.data', 'r') as file_handler:
    for line in file_handler:
        xys += [[int(line.split(' ')[0]), int(line.split(' ')[1])]]

columns = ['X', 'Y']
labels = [str(i) for i in range(len(xys))]
labels_cpy = labels.copy()

points = pd.DataFrame(xys, columns=columns, index=labels)

dists_orig = pd.DataFrame(squareform(pdist(points, metric='euclidean')), columns=labels, index=labels)
# print(dists_orig.head(10))

dists = dists_orig.copy()
# dists.to_csv('distances.csv')


n_groups = 10
groups = {}
for elem in range(n_groups):
    groups['g'+str(elem)] = []

random.seed(5)  # TODO: remove
for group in groups.keys():
    temp = random.choice(labels_cpy)

    groups[group].append(temp)
    labels_cpy.remove(temp)
    dists.drop(temp, axis=0, inplace=True)

print(f'Randomized: {groups}')

# for key in groups.keys():
#     temporary = dists.nsmallest(1, columns=[groups[key][0]]).index[0]
#     print(temporary)
#     groups[key].append(temporary)
#     dists.drop(temporary, axis=0, inplace=True)

while len(dists):
    for grp in groups.items():
        # print(grp[1])
        l = []

        for elem in grp[1]:
            try:
                l.append(dists.nsmallest(1, columns=[elem]))
            except IndexError:
                break

        try:
            x = collections.Counter(l).most_common(1)[0]
            print(f"Lista: {l}, srednia: {srednia(l)},\n x: {x}")#, x<srednia: {x<mean(l)}")

            dists.drop(x[0], axis=0, inplace=True)
            grp[1].append(x[0])
        except IndexError as ie:
            print(ie)
            break
print(f'Groups: {groups}')


plt.xlabel('X')
plt.ylabel('Y')

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

cntr = 0
for i in groups.items():
    x = []
    y = []
    for e in i[1]:
        x.append(points.loc[e, 'X'])
        y.append(points.loc[e, 'Y'])

    plt.scatter(
        x,
        y,
        c=colors[cntr]
    )
    cntr += 1

plt.show()

#     plt.plot(curr_plot, 'go')
#     plt.show()
#
# print(points)
# plt.plot(points, 'ro')
# plt.xticks(np.arange(0, len(xys), 20.0))  # Pick every n-th x axis' value
# plt.show()
