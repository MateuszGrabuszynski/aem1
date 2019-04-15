import random as rd
import pandas as pd
import time

import matplotlib.pyplot as plt

###
points = pd.read_csv('objects.data', sep=" ", header=None, usecols=[0, 1])
points.columns = ['X', 'Y']
print(points)
x = []
y = []
clrs = []
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
          'tab:olive', 'tab:cyan']

for i in range(len(points)):
    x.append(points.iloc[i][0])
    y.append(points.iloc[i][1])
    clrs.append(colors[0])

print("x:", x)
print("y:", y)
###

start_time = time.time()
GROUPS = 20
POINTS = 423
#rd.seed(65)
# Read distances
distances = pd.read_csv('distances.csv', sep=',', dtype=float, usecols=range(0, POINTS+1)) # usecols=Omit the index column
print(distances.columns)
distances_cpy = distances.copy()

print(distances)

cols = []
for i in range(POINTS):
    col = distances_cpy.sort_values(by=[str(i)])
    cols.append(col[str(i)])  # .iloc[1:])

# Points that are still available as endings
not_available_ending_points = set()


points = list(range(0, POINTS))
groups = list(range(0, GROUPS))
dictionaries = dict.fromkeys(groups, set())

copy_point = points.copy()

for group in dictionaries.keys():
    value = rd.choice(copy_point)
    dictionaries[group] = {(value, value)}
    # print(copy_point)
    copy_point.remove(value)
    # print(copy_point)
    not_available_ending_points.add(value)


while len(not_available_ending_points) < POINTS:

    current_shortest_edge = {
        'group': None,
        'from_point': None,
        'to_point': None,
        'distance': None
    }

    for group in dictionaries.keys():
        # print("Group:", group)
        for _, point_in_group in dictionaries[group]:
            # print("Point_in_group:", point_in_group)
            for new_point, dist in cols[point_in_group].sort_values(ascending=True).iteritems():
                # print(new_point, dist)
                if new_point not in not_available_ending_points:
                    if current_shortest_edge['distance'] is None or dist < current_shortest_edge['distance']:
                        current_shortest_edge['group'] = group
                        current_shortest_edge['from_point'] = point_in_group
                        current_shortest_edge['to_point'] = new_point
                        current_shortest_edge['distance'] = dist

    if current_shortest_edge['to_point'] is not None:
        # print('jestem tutaj!')
        not_available_ending_points.add(current_shortest_edge['to_point'])
        for group in dictionaries.keys():
            for _, point_in_group in dictionaries[group]:
                cols[point_in_group].drop(current_shortest_edge['to_point'], inplace=True)

        dictionaries[current_shortest_edge['group']].add((current_shortest_edge['from_point'], current_shortest_edge['to_point']))
        current_shortest_edge['group'] = None
        current_shortest_edge['from_point'] = None
        current_shortest_edge['to_point'] = None
        current_shortest_edge['distance'] = None

print("dicti", dictionaries)
elapsed_time = time.time() - start_time
print(elapsed_time)

edges = dictionaries

clr_nr = 0
for grp in edges.values():
    for case in grp:
        pointa_x = x[case[0]]
        pointa_y = y[case[0]]
        pointb_x = x[case[1]]
        pointb_y = y[case[1]]

        plt.plot([pointa_x, pointb_x], [pointa_y, pointb_y], marker='o', c=colors[clr_nr])#, marker='o')
    clr_nr += 1

plt.xlabel('X')
plt.ylabel('Y')

plt.show()