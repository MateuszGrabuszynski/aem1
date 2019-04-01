import random as rd
import pandas as pd
import time

import matplotlib.pyplot as plt

###
points = pd.read_csv('objects.data', sep=" ", header=None, usecols=[0, 1])
points.columns = ['X', 'Y']

x = []
y = []
clrs = []
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
          'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

for i in range(len(points)):
    x.append(points.iloc[i][0])
    y.append(points.iloc[i][1])
    clrs.append(colors[0])
###

start_time = time.time()
GROUPS = 10
POINTS = 201
rd.seed(65)

full_dist = 0
no_edges = 0

# Read distances
distances = pd.read_csv('distances.data', usecols=range(0, POINTS + 1))  # usecols=Omit the index column
distances_cpy = distances.copy()

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

is_second = False

first_matched_point = {
    'group': None,
    'from_point': None,
    'to_point': None,
    'distance': None
}
second_matched_point = {
    'group': None,
    'from_point': None,
    'to_point': None,
    'distance': None
}


while len(not_available_ending_points) < POINTS:
    current_shortest_edge = {
        'group': None,
        'from_point': None,
        'to_point': None,
        'distance': None
    }

    for group in dictionaries.keys():
        #print("Group:", group)
        for _, point_in_group in dictionaries[group]:
            #print("Point_in_group:", point_in_group)
            for new_point, dist in cols[point_in_group].sort_values(ascending=True).iteritems():
                #print(new_point, dist)
                if new_point not in not_available_ending_points:
                    if current_shortest_edge['distance'] is None or dist < current_shortest_edge['distance']:
                        current_shortest_edge['group'] = group
                        current_shortest_edge['from_point'] = point_in_group
                        current_shortest_edge['to_point'] = new_point
                        current_shortest_edge['distance'] = dist

    if current_shortest_edge['to_point'] is not None:
        if is_second is False:
            first_matched_point = {
                'group': current_shortest_edge['group'],
                'from_point': current_shortest_edge['from_point'],
                'to_point': current_shortest_edge['to_point'],
                'distance': current_shortest_edge['distance'],
            }
            # not_available_ending_points.add(current_shortest_edge['to_point'])

            current_shortest_edge['group'] = None
            current_shortest_edge['from_point'] = None
            current_shortest_edge['to_point'] = None
            current_shortest_edge['distance'] = None

            # print("\nMam 1pkt point", first_matched_point)
            is_second = True
            # print('Flaga na :', is_second)
            # print("Dodaje ten punkt do not_available_ending_points", first_matched_point['to_point'])
            # not_available_ending_points.add(first_matched_point['to_point'])

            print("not_available:", not_available_ending_points)
        else:
            second_matched_point = {
                'group': current_shortest_edge['group'],
                'from_point': current_shortest_edge['from_point'],
                'to_point': current_shortest_edge['to_point'],
                'distance': current_shortest_edge['distance'],
            }

            not_available_ending_points.add(second_matched_point['to_point'])
            not_available_ending_points.remove(first_matched_point['to_point'])


            dictionaries[second_matched_point['group']].add(
                (second_matched_point['from_point'], second_matched_point['to_point'])
            )
            #full_dist += second_matched_point['distance']
            #no_edges += 1

            # inna grupa po prostu
            zielona_grupa = second_matched_point['group']

            for _, point_in_group in dictionaries[zielona_grupa]:
               # print("Point_in_group:", point_in_group)
                for new_point, dist in cols[point_in_group].sort_values(ascending=True).iteritems():
                   # print(new_point, dist)
                    if new_point not in not_available_ending_points:
                        if current_shortest_edge['distance'] is None or dist < current_shortest_edge['distance']:
                            current_shortest_edge['group'] = zielona_grupa
                            current_shortest_edge['from_point'] = point_in_group
                            current_shortest_edge['to_point'] = new_point
                            current_shortest_edge['distance'] = dist

            #print("Mam 3pkt:", current_shortest_edge)
            if current_shortest_edge['to_point'] != first_matched_point['to_point']:
                dictionaries[first_matched_point['group']].add(
                    (first_matched_point['from_point'], first_matched_point['to_point']))

                #full_dist += first_matched_point['distance']
                #no_edges += 1

                #dictionaries[current_shortest_edge['group']].add(
                #    (current_shortest_edge['from_point'], current_shortest_edge['to_point'])
                #)

                #full_dist += current_shortest_edge['distance']
                #no_edges += 1


                not_available_ending_points.add(
                    first_matched_point['to_point']
                )
                #not_available_ending_points.add(
                #    current_shortest_edge['to_point']
                #)

            elif current_shortest_edge['to_point'] == first_matched_point['to_point'] \
                    and current_shortest_edge['group'] != first_matched_point['group']:

                if first_matched_point['distance'] < current_shortest_edge['distance']:
                    dictionaries[first_matched_point['group']].add(
                        (first_matched_point['from_point'], first_matched_point['to_point']))

                    #full_dist += first_matched_point['distance']
                    #no_edges += 1

                    dictionaries[second_matched_point['group']].remove(
                        (second_matched_point['from_point'], second_matched_point['to_point'])
                    )

                    #full_dist -= second_matched_point['distance']
                    #no_edges -= 1

                    not_available_ending_points.add(first_matched_point['to_point'])
                    not_available_ending_points.remove(second_matched_point['to_point'])
                else:
                    """ 
                        wszystko do drugiej grupy bo rozrosła się na tyle zeby wziąc pierwszy
                        odłożony punkt
                    """
                    dictionaries[current_shortest_edge['group']].add(
                        (current_shortest_edge['from_point'], current_shortest_edge['to_point'])
                    )

                    #full_dist += current_shortest_edge['distance']
                    #no_edges += 1

                    dictionaries[current_shortest_edge['group']].add(
                        (first_matched_point['from_point'], first_matched_point['to_point'])
                    )
                   # full_dist += first_matched_point['distance']
                   # no_edges += 1

                    not_available_ending_points.add(
                        first_matched_point['to_point']
                    )
                    not_available_ending_points.add(
                        current_shortest_edge['to_point']
                    )


            is_second = False

            first_matched_point['group'] = None
            first_matched_point['from_point'] = None
            first_matched_point['to_point'] = None
            first_matched_point['distance'] = None

            second_matched_point['group'] = None
            second_matched_point['from_point'] = None
            second_matched_point['to_point'] = None
            second_matched_point['distance'] = None

            current_shortest_edge['group'] = None
            current_shortest_edge['from_point'] = None
            current_shortest_edge['to_point'] = None
            current_shortest_edge['distance'] = None


elapsed_time = time.time() - start_time
print(elapsed_time)

edges = dictionaries.copy()
counter_edges = 0
for gr in edges.keys():
    counter_edges += len(edges[gr])

clr_nr = 0
firsts = []

the_same = 0
whole_dist = 0
for gr in edges.keys():
    if len(edges[gr]) == 1:
        print([gr], edges[gr])
    for point in edges[gr]:
        whole_dist += cols[point[0]][point[1]]
        if point[0] == point[1]:
            the_same += 1

egdes_num = counter_edges-the_same
print("Edge num:", egdes_num)
print("Whole_dist:", whole_dist)
print("Avg_dist:", whole_dist/egdes_num)
print("Time", elapsed_time)

for grp in edges.values():
    first = True
    for case in grp:
        pointa_x = x[case[0]]
        pointa_y = y[case[0]]

        pointb_x = x[case[1]]
        pointb_y = y[case[1]]
        plt.plot([pointa_x, pointb_x], [pointa_y, pointb_y], c=colors[clr_nr], marker='o')

        if first:
            firsts.append((pointa_x, pointa_y))
        first = False

    clr_nr += 1

for el in firsts:
    plt.scatter(
        el[0],
        el[1],
        marker='o'
    )

plt.xlabel('X')
plt.ylabel('Y')


plt.savefig('wynik.png')
plt.show()




the_same = 0
whole_dist = 0

for gr in edges.keys():

    if len(edges[gr]) == 1:
        #print([gr], edges[gr])
        continue
    for point in edges[gr]:
        whole_dist += cols[point[0]][point[1]]
        if point[0] == point[1]:
            the_same += 1