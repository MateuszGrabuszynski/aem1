import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from scipy.spatial.distance import pdist, squareform

xys = []

with open('objects.data', 'r') as file_handler:
    for line in file_handler:
        xys += [[int(line.split(' ')[0]), int(line.split(' ')[1])]]

columns = ['X', 'Y']
labels = [str(i) for i in range(len(xys))]

points = pd.DataFrame(xys, columns=columns, index=labels)
# print(points)

dists_orig = pd.DataFrame(squareform(pdist(points, metric='euclidean')), columns=labels, index=labels)
dists = dists_orig.copy()
# dists.to_csv('distances.csv')
# print(dists)

n_groups = 10
groups = {}
for i in range(n_groups):
    temp = random.choice(labels)
    if temp not in groups:
        groups[temp] = []
        dists.drop(str(temp), axis=0, inplace=True)
    else:
        i -= 1
print(f'Randomized: {groups}')
# print(dists)

for i in range(20):
    for key in groups.keys():
        # print('Column:', key)
        try:
            temporary = dists.nsmallest(2, columns=[key] + groups[key]).index[0]
            # minim = 500
            # temporary = []
            # for k in [key]+groups[key]:
            #     tmp = dists[k].min()
            #     if tmp < minim:
            #         temporary = [dists[k][0]]
            #         minim = tmp
            # print('Temporary:', temporary)
            groups[key] += [temporary]
            dists.drop(str(temporary), axis=0, inplace=True)
            # print('Groups:', [key] + groups[key])
        except IndexError:
            break

plots = {}
x=97
for key in groups.keys():
    print('Groups:', [key] + groups[key])
    curr_plot = []

    # print points
    curr_plot += [[points.loc[key, :][0], points.loc[key, :][1]]]
    for val in groups[key]:
        curr_plot += [[points.loc[val, :][0], points.loc[val, :][1]]]

    print(curr_plot)
    plots[chr(x)] = curr_plot
    x += 1


plt.scatter(
    points['X'],
    points['Y'],
    c=np.random.rand(201),#2*np.pi*np.random.rand(201),
    s=25,
    data=plots
)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

#     plt.plot(curr_plot, 'go')
#     plt.show()
#
# print(points)
# plt.plot(points, 'ro')
# plt.xticks(np.arange(0, len(xys), 20.0))  # Pick every n-th x axis' value
# plt.show()
