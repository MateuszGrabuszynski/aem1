import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans


xys = []

with open('objects.data', 'r') as file_handler:
    for line in file_handler:
        xys += [[int(line.split(' ')[0]), int(line.split(' ')[1])]]

columns = ['X', 'Y']
labels = [str(i) for i in range(len(xys))]
labels_cpy = labels.copy()

points = pd.DataFrame(xys, columns=columns, index=labels)

dists_orig = pd.DataFrame(squareform(pdist(points, metric='euclidean')), columns=labels, index=labels)

dists = dists_orig.copy()
# dists.to_csv('distances.csv')

km = KMeans(n_clusters=10,
            init='random',
            n_init=10,
            max_iter=300,
            tol=1e-04,
            random_state=0)

y_km = km.fit_predict(points)


x = []
y = []
clrs = []
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
          'tab:olive', 'tab:cyan']

# for i in range(len(points)):
#     x.append(points.iloc[i][0])
#     y.append(points.iloc[i][1])
#     clrs.append(colors[y_km[i]])
#
# plt.scatter(
#     x,
#     y,
#     c=clrs
# )
#
# plt.xlabel('X')
# plt.ylabel('Y')
#
# plt.show()


pts = pd.DataFrame({
    'point': points.index,
    'x': points['X'],
    'y': points['Y'],
    'gr': y_km
})
print(pts)

gr_dists = []
for i in range(10):
    gr_points = pts.loc[pts['gr'] == i]['point']
    # print(gr_points.values.tolist())
    gr_dists.append(dists_orig[gr_points.values.tolist()].loc[gr_points.values.tolist()])
    # print(i)
    # print(gr_dists[i])
    print(random.choice(gr_points))


