import pandas as pd

from scipy.spatial.distance import pdist, squareform

# Reading file with objects
objects = pd.read_csv('objects.data', sep=" ", header=None, usecols=[0, 1])
objects.columns = ['X', 'Y']
print(objects.head())

# Counting distances
no_objects = [x for x in range(len(objects.index))]
distances = pd.DataFrame(squareform(pdist(objects, metric='euclidean')), columns=no_objects, index=no_objects)
print(distances.head())

distances.to_csv('distances.data')





