# Libraries Included:
# Numpy, Scipy, Scikit, Pandas
import pandas as pd
import copy

# inputs

mices = [6, 2, 8, 9]
holes = [(3,6),(2,1),(3,6),(4,7),(4,7)]
# mices = [10, 20, 30, 40, 50, 45, 35]
# holes = [(-1000000000,10),(1000000000,1)]

def clean_hole(holes):
    length_holes = {}

    for j,c in holes:
        if j in list(length_holes.keys()):
            length_holes[j] += c
        else:
            length_holes[j] = c
    return length_holes


def search_subida_montanha(mices,holes):
    length_holes = clean_hole(holes)
    keys = ('floor','mices','holes','cost')

    mices_left = mices
    holes_state = {}
    for hole,_ in holes:
        holes_state.setdefault(hole,[])

    node_to_climb = {"floor": 0, "mices": mices_left, "holes": holes_state, "cost": 0}
    total_cost = 0

    for floor in range(1,1+len(mices)):
        print "FLOOR", floor
        print ""
        print "CURRENT NODE", node_to_climb
        print ""
        list_of_nodes_in_floor = []     # for each floor, creates a list of possible nodes

        prev_mices_left = node_to_climb['mices']         # save prev mices and holes
        prev_holes_state = node_to_climb['holes']

        for index,mice in enumerate(prev_mices_left):       # calculates each possible node and append it to list_of_nodes_in_floor

            for hole in prev_holes_state:
                current_holes_state = copy.deepcopy(prev_holes_state)
                if len(current_holes_state[hole]) < length_holes[hole]:
                    current_holes_state[hole].append(mice)
                    current_mices_left = [m for k,m in enumerate(prev_mices_left) if index != k]
                    current_cost = abs(mice - hole)
                    dict_to_append = {"floor": floor, "mices": current_mices_left, "holes": current_holes_state, "cost": current_cost}
                    list_of_nodes_in_floor.append(dict_to_append)

        # sort list_of_nodes_in_floor by cost
        sorted_nodes_in_floor = sorted(list_of_nodes_in_floor, key = lambda node: node['cost'])
        print "SORTED NODES IN FLOOR", sorted_nodes_in_floor
        print ""
        # picks the next node by the lower cost
        node_to_climb = sorted_nodes_in_floor[0]
        print "NEW NODE TO CLIMB", node_to_climb
        print ""
        # increment total_cost
        total_cost += node_to_climb["cost"]
        print "TOTAL COST", total_cost
        print ""
        print "############"
        print ""

    return total_cost

print search_subida_montanha(mices,holes)
