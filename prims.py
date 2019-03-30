import random as rd
import pandas as pd

GROUPS = 10
POINTS = 200

# Read distances
distances = pd.read_csv('distances.data', usecols=range(1, POINTS + 2))  # usecols=Omit the index column
print(distances.head())
distances_cpy = distances.copy()

cols = []
for i in range(POINTS):
    col = distances_cpy.sort_values(by=[str(i)])
    cols.append(col[str(i)].iloc[1:])
print(cols)

# # Get the longest distance from distances
# longest_distance = max(distances.max(axis=1))+1  # +1 for < operation instead of <=

# Points that are still available as endings
not_available_ending_points = []

# Create tree tables with randomly chosen points
# trees = [(point_from, point_to, distance), (...),...]
trees = []
for i in range(GROUPS):
    cont = False
    value = 0
    while True:
        value = rd.randint(0, POINTS)
        for tree in trees:
            if tree['point_from'] == value:
                cont = True
        if not cont:
            break

    trees.append({
        'tree_nr': i,
        'point_from': value,
        'point_to': None,
        'distance': None
    })
    # trees = [ {}, {}, {}, ... ]
    not_available_ending_points.append(value)
print(trees)

while len(not_available_ending_points) <= POINTS:
    current_shortest_edge = {
        'tree_nr': None,
        'point_from': None,
        'point_to': None,
        'distance': None
    }
    xyz = {
        'tree_nr': None,
        'point_from': None,
        'point_to': None,
        'distance': None
    }
    for tree_element in trees:  # {..}
        for dist_tab in cols[tree_element['point_from']]:
            for dist in dist_tab[0]:
                if current_shortest_edge['distance'] is None or dist.iloc[1] <= current_shortest_edge['distance']:
                    if dist.iloc[1] not in not_available_ending_points:
                        current_shortest_edge = {
                            'tree_nr': tree_element['group'],
                            'point_from': tree_element['point_from'],
                            'point_to': dist.iloc[0],
                            'distance': dist.iloc[1]
                        }
                        xyz = tree_element
    trees.append(current_shortest_edge)
    not_available_ending_points.append(current_shortest_edge['point_to'])
    print(trees)




# # Looks in columns (distances[point]) for shortest distances
# for _ in range(20):
#     curr_min = (None, longest_distance, None)
#     append_value_to_tree = 0
#     for t in range(GROUPS):
#         for point in trees[t]:
#             # (X, _, _) / point[0]
#             dist = distances[str(point[0])].nsmallest(2)
#             dist_value = dist.iloc[-1]
#             if dist_value < curr_min[1]:
#                 curr_min = (point[0], dist_value, dist.index[1])
#                 append_value_to_tree = t
#
#             # (_, _, X) / point[2]
#             if point[2]:
#                 dist = distances[str(point[2])].nsmallest(2)
#                 dist_value = dist.iloc[-1]
#                 if dist_value < curr_min[1]:
#                     curr_min = (point[2], dist_value, dist.index[1])
#                     append_value_to_tree = t
#
#     print(f'Append to tree {t} given tuple: {curr_min}')
#     print(trees)
#
#     # Appending to the tree...
#     if trees[append_value_to_tree][0] != curr_min[0]:
#         trees[append_value_to_tree].append(curr_min)
#     else:
#         trees[append_value_to_tree][0] = curr_min
#
#     print(trees)




