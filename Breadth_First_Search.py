# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import copy

# mices = [6, 2, 8, 9]
# holes = [(3,6),(2,1),(3,6),(4,7),(4,7)]
mices = [10, 20, 30, 40, 50, 45, 35]

holes = [(-1000000000, 10), (1000000000, 1)]


def clean_hole(holes):
    length_holes = {}

    for j, c in holes:
        if j in list(length_holes.keys()):
            length_holes[j] += c
        else:
            length_holes[j] = c
    return length_holes


def search(mices, holes):
    list_of_dicts = []
    length_holes = clean_hole(holes)
    keys = ('floor', 'mices', 'holes', 'cost')

    mices_left = mices
    holes_state = {}
    for hole, _ in holes:
        holes_state.setdefault(hole, [])

    dict_to_append = {"floor": 0, "mices": mices_left, "holes": holes_state, "cost": 0}
    list_of_dicts.append(dict_to_append)

    first_index_of_floor = 0
    node_index = 0
    floor_indexes = {0: 0, 1: 1}
    for floor in range(1, 1 + len(mices)):

        sub_list_of_dicts = list_of_dicts[floor_indexes[floor - 1]:]

        for node in sub_list_of_dicts:
            prev_mices_left = node['mices']
            prev_holes_state = node['holes']
            prev_cost = node['cost']
            for index, mice in enumerate(prev_mices_left):

                for hole in prev_holes_state:
                    current_holes_state = copy.deepcopy(prev_holes_state)
                    if len(current_holes_state[hole]) < length_holes[hole]:
                        current_holes_state[hole].append(mice)
                        current_mices_left = [m for k, m in enumerate(prev_mices_left) if index != k]
                        current_cost = prev_cost + abs(mice - hole)
                        dict_to_append = {"floor": floor, "mices": current_mices_left, "holes": current_holes_state,
                                          "cost": current_cost}
                        list_of_dicts.append(dict_to_append)
                        node_index += 1

        floor_indexes[floor + 1] = node_index + 1

    last_floor_list = list_of_dicts[floor_indexes[len(mices)]:]
    list_of_costs = [node["cost"] for node in last_floor_list]

    return min(list_of_costs)


print search(mices, holes)