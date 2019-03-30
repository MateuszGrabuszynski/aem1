import random as rd
import pandas as pd
import time

start_time = time.time()
GROUPS = 10
POINTS = 201
rd.seed(65)
# Read distances
distances = pd.read_csv('distances.data', usecols=range(1, POINTS + 2))  # usecols=Omit the index column
distances_cpy = distances.copy()

cols = []
for i in range(POINTS):
	col = distances_cpy.sort_values(by=[str(i)])
	cols.append(col[str(i)])  # .iloc[1:])

# Points that are still available as endings
not_available_ending_points = []


points = list(range(0, POINTS))
groups = list(range(0, GROUPS))
dictionaries = dict.fromkeys(groups, list())

copy_point = points.copy()

for group in dictionaries.keys():
	value = rd.choice(copy_point)
	dictionaries[group] = [(value, value)]
	# print(copy_point)
	copy_point.remove(value)
	# print(copy_point)
	not_available_ending_points.append(value)


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
			not_available_ending_points.append(current_shortest_edge['to_point'])
			for group in dictionaries.keys():
				for _, point_in_group in dictionaries[group]:
					#print("Drop", point_in_group, current_shortest_edge['to_point'])
					cols[point_in_group].drop(current_shortest_edge['to_point'], inplace=True)

			# print(type(cols[point_in_group]))

			dictionaries[current_shortest_edge['group']].append((current_shortest_edge['from_point'], current_shortest_edge['to_point']))
			current_shortest_edge['group'] = None
			current_shortest_edge['from_point'] = None
			current_shortest_edge['to_point'] = None
			current_shortest_edge['distance'] = None

print("dicti", dictionaries)
elapsed_time = time.time() - start_time
print(elapsed_time)