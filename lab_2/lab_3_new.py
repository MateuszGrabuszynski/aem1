import sys
import time
import numpy as np
import pandas as pd
import random
from collections import Counter
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

import itertools
from itertools import chain

def delta_cost(orginal_set, orginal_set2, new_set1, new_set2):
    pass


def get_set_of_points(lsts):
    return set(chain.from_iterable(lsts))


def get_tree_size(tree, distance):
    tree_size = 0
    tree_path = 0
    for x, y in tree:
        tree_size += 1
        tree_path += distance[(x, y)]
    return {
        "tree_size": tree_size,
        "tree_path": tree_path
    }


def prim(groups_with_points, dict_distances):
    groups = groups_with_points.keys()
    trees = dict()

    tree_path = dict()
    for group in groups:
        # create tree dict to save tree
        trees[group] = []
        # Get points for grouptrees
        points = list(groups_with_points[group])
        # print(points)
        # print(distances_for_group)

        # Get number of points
        number_of_points = len(points)
        # print(number_of_points)

        # Set set for added points yet
        added_points = set()

        # Start by random point
        current_point = points[0]

        # print("Current point:", current_point)
        # Add to just added points
        added_points.add(current_point)
        # print(added_points)

        # print(cols)
        # print("group:", group, "\n", cols[group][0])
        while len(added_points) < number_of_points:

            shortest_edge = {
                'group': None,
                'from_point': None,
                'to_point': None,
                'distance': None
            }

            for added_point in added_points:
                for new_point in points:
                    dist = dict_distances[(added_point, new_point)]
                    if new_point != added_point and new_point not in added_points:
                        if shortest_edge['distance'] is None or dist < shortest_edge['distance']:
                            shortest_edge['group'] = group
                            shortest_edge['from_point'] = added_point
                            shortest_edge['to_point'] = new_point
                            shortest_edge['distance'] = dist

            trees[shortest_edge['group']].append(
                [shortest_edge['from_point'],
                 shortest_edge['to_point']])

            added_points.add(shortest_edge['to_point'])
            shortest_edge['group'] = None
            shortest_edge['from_point'] = None
            shortest_edge['to_point'] = None
            shortest_edge['distance'] = None

        trees[group].sort()
    return trees


def time_measurement(function, args_for_func):
    """
        Function to measure time
    """
    start = time.time()
    function(*args_for_func)
    end = time.time()
    return end - start


def load_data(filename):
    """Wczytanie danych"""
    objects = pd.read_csv(filename, names=["x", "y"], sep=" ", header=None, dtype=int)
    return objects


def create_distance_matrix(data):
    no_objects = [x for x in range(len(data))]
    distances = pd.DataFrame(squareform(pdist(data, metric='euclidean')), columns=no_objects, index=no_objects, dtype=float)

    # print(distances)
    return distances


def gen_random_groups(data_len, num_groups=20):
    i = 0
    points = np.array((range(data_len)))
    # indicies
    points_permutation = np.random.permutation(points)
    clusters = np.ones(data_len, dtype=np.int) * (-1)
    for index in points_permutation:
        if i == num_groups:
            i = 0
        clusters[index] = i
        i += 1

    return clusters


def measure_edges(set_of_points, dict_distance):
    sum = 0
    edges = set(itertools.product(set_of_points, set_of_points))
    for edge in edges:
        # print(edge)
        # print(dict_distance[edge])
        sum += dict_distance[edge]
    return sum


def get_info_about_trees(trees, dict_distance):
    trees_infos = dict()
    tree_info = {
        "points": None,
        "num_of_points": None,
        "num_of_edges": None,
        "cost": None
    }

    for key, tree in trees.items():
        trees_infos[key] = None
        # only points
        tree_info['points'] = get_set_of_points(tree)
        # num of points
        tree_info['num_of_points'] = len(tree_info['points'])
        # num of edges
        tree_info['num_of_edges'] = len(set(itertools.product(tree_info['points'],
                                                              tree_info['points'])))
        # Count cost of tree
        tree_info['cost'] = measure_edges(tree_info['points'], dict_distance)

        trees_infos[key] = tree_info

    return trees_infos


def get_points_for_group(dict_points, group):
    points_in_group = set()
    items = dict_points.items()
    for point_id, point_group in items:
        if point_group == group:
            points_in_group.add(point_id)
    return points_in_group


def get_cost(tree, matrix_distance):
    # przed wyciągnięciem
    set0_sum = 0

    points = list(tree)
    # print(points)
    elem = matrix_distance.iloc[points, points]
    n = len(elem)
    edges = (n * (n - 1)) / 2
    res = matrix_distance.iloc[points, points].sum().sum() / 2

    return res, edges


def get_sets(points, moved_point, old_group, new_group):
    keys = {0, 1, 2, 3}
    sets = dict()
    for key in keys:
        sets[key] = []

    items = points.items()
    for point_id, group in items:
        if group == old_group:
            sets[0].append(point_id)

        elif group == new_group:
            sets[1].append(point_id)

    sets[2] = sets[0].copy()

    sets[2].remove(moved_point)

    sets[3] = sets[1].copy()
    sets[3].append(moved_point)

    return sets

def find_neigbourhood_groups(point, neigbourhood):
    global dict_distances
    global points_dict
    global matrix_distance
   # print(matrix_distance)
    filtr = matrix_distance[point] < neigbourhood
    current_neighborhood = matrix_distance[point][filtr]

    neighbourhood_groups = set()
    for ind in current_neighborhood.index:
         neighbourhood_groups.add(points_dict[ind])

    # remove the same group
    neighbourhood_groups.remove(points_dict[point])
    return list(neighbourhood_groups)



def steepst(trees, neighbourhood):
    global dict_distances
    global matrix_distance
    points_dict = dict()
    groups = list(trees.keys())

    costs = dict()
    edges = dict()
    for key, tree in trees.items():
        points = get_set_of_points(tree)
        costs[key], edges[key] = get_cost(points, matrix_distance)
        for point in points:
            points_dict[point] = key

    # print(points_dict)

    # point is key, current_group is value

    move_point = dict()
    # Punkt który jest analizowany
    move_point["point"] = None

    # Grupa
    move_point["new_group"] = None

    # Grupa do której należy
    move_point["orginal_group"] = None


    for point, old_group in points_dict.items():
        move_point["orginal_group"] = old_group
        move_point["point"] = point

        current_deltas = set()  # delty
        to_be_moved_group = dict()  # grupa tego punktu

        to_be_moved_group['new_group'] = None
        to_be_moved_group['delta'] = None
        to_be_moved_group['new_2'] = None
        to_be_moved_group['new_3'] = None
        to_be_moved_group['new_num_edges_2'] = None
        to_be_moved_group['new_num_edges_3'] = None


        for new_group in groups:
            if old_group != new_group:

                move_point["orginal_group"] = old_group
                move_point["new_group"] = new_group

                # print(move_point)
                # Get current state of groups
                sets = get_sets(points_dict, move_point['point'], old_group, new_group)
                # Przed zabraniem
                # print("Cost:", get_cost(sets[0], matrix_distance))
                # Przed dodaniem
                # print("Cost:", get_cost(sets[1], matrix_distance))
                # Po zabraniu
                # print("Cost:", get_cost(sets[2], matrix_distance))
                # Po dodaniu
                # print("Cost:", get_cost(sets[3], matrix_distance))
                # old_0, old_num_egdes_0 = get_cost(sets[0], matrix_distance)
                # old_1, old_num_egdes_1 = get_cost(sets[1], matrix_distance)

                new_2, new_num_edges_2 = get_cost(sets[2], matrix_distance)
                new_3, new_num_edges_3 = get_cost(sets[3], matrix_distance)

                if new_num_edges_2 == 0 or new_num_edges_3 == 0:
                    break

                # cost_new = new_2 + new_3
                # edges_new = new_num_edges_2 + new_num_edges_3

                test_costs = costs.copy()
                test_edges = edges.copy()

                test_costs[old_group] = new_2
                test_edges[old_group] = new_num_edges_2

                test_costs[new_group] = new_3
                test_edges[new_group] = new_num_edges_3


                old_stat = sum(costs.values()) / sum(edges.values())
                test_stat = sum(test_costs.values()) / sum(test_edges.values())

                if old_stat > test_stat:
                                           # koszt starych drzew - koszt nowych drzew
                    if to_be_moved_group['delta'] is None or (old_stat - test_stat) > to_be_moved_group['delta']:

                        to_be_moved_group['new_group'] = move_point['new_group']
                        to_be_moved_group['delta'] = old_stat-test_stat
                        to_be_moved_group['new_2'] = new_2
                        to_be_moved_group['new_3'] = new_3
                        to_be_moved_group['new_num_edges_2'] = new_num_edges_2
                        to_be_moved_group['new_num_edges_3'] = new_num_edges_3

        # optimise
        if to_be_moved_group['delta'] is None:
            continue
        else:
            points_group = to_be_moved_group['new_group']
            new2 = to_be_moved_group['new_2']
            new3 = to_be_moved_group['new_3']
            nne2 = to_be_moved_group['new_num_edges_2']
            nne3 = to_be_moved_group['new_num_edges_3']


            points_dict[move_point['point']] = points_group
            # print(move_point['point'], '..', move_point['new_group'])

            costs[old_group], edges[old_group] = new2, nne2
            costs[points_group], edges[points_group] = new3, nne3


            move_point["new_group"] = None
            move_point["orginal_group"] = None
            move_point["point"] = None

            to_be_moved_group['new_group'] = None
            to_be_moved_group['new_2'] = None
            to_be_moved_group['new_3'] = None
            to_be_moved_group['new_num_edges_2'] = None
            to_be_moved_group['new_num_edges_3'] = None

    for gr in range(20):
        print('gr {}: {}'.format(gr, get_points_for_group(points_dict, gr)))
    print("SUM:", sum(costs.values()) / sum(edges.values()))


def run(groups, dist_matrix, neighbourhood=100):
    n_groups = len(groups)


dict_distances = dict()
matrix_distance = None
points_dict = dict()

def main():
    global matrix_distance
    global dict_distances
    global points_dict
    # option_tree, method = sys.argv
    option_tree = "random"
    method = "greedy"
    data = load_data('objects.data')
    data_len = len(data)
    n_groups = 20
    matrix_distance = create_distance_matrix(data)

    matrix_distance_cpy = matrix_distance.copy()
    dict_distances = dict()

    for (x, y), dist in np.ndenumerate(matrix_distance_cpy):
        dict_distances[x, y] = dist

    # print(dict_distances)
    x = []
    y = []
    clrs = []

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan']

    for i in range(len(matrix_distance_cpy)):
        x.append(matrix_distance_cpy.iloc[i][0])
        y.append(matrix_distance_cpy.iloc[i][1])
        # clrs.append(colors[i])

    # print(matrix_distance)
    matrix_distance.to_csv("distances.csv", sep=",", index=False, columns=list(range(data_len)))

    if option_tree == "prim":
        pass
        # trees =
        # tree_keys = trees.keys()
        # for key in tree_keys:
        #     get_tree_size(trees[key], dict_distances)
        #
        # neigbourhood = 30
        #
        # for key, tree in trees.items():
        #     points = get_set_of_points(tree)
        #     for point in points:
        #         points_dict[point] = key
        #
        # greedy_trees = greedy(trees, neigbourhood)
        #
        # steepst_trees = steepst(trees, neigbourhood)

    elif option_tree == "random":

        # random.seed(5)
        # np.random.seed(5)

        random_list_of_groups = gen_random_groups(data_len, n_groups)
        # print(random_list_of_groups)

        # print("random", Counter(random_list_of_groups))
        points_in_groups = dict()

        """
              x  y    x y
        0: { (34,2), (5,6),... }, ..., 19: { ...}

        """
        for group in range(n_groups):
            points_in_groups[group] = set()

        # point return like np.array from pandas
        data_matrix = data.values

        for index, group in enumerate(random_list_of_groups):
            # print(index, group)
            # points_in_groups[group].add((data_matrix[index][0], data_matrix[index][1]))
            points_in_groups[group].add(index)  # list of points

            # create_prim()
            # print(points_in_groups)
        print(points_in_groups)

        trees = prim(points_in_groups, dict_distances)
        # print(trees)
        tree_keys = trees.keys()
        for key in tree_keys:
            get_tree_size(trees[key], dict_distances)

        neigbourhood = 30

        for key, tree in trees.items():
            points = get_set_of_points(tree)
            for point in points:
                points_dict[point] = key

        #greedy_trees = greedy(trees, neigbourhood)

        steepst_trees = steepst(trees, neigbourhood)


if __name__ == "__main__":
    print(time_measurement(main, []))
