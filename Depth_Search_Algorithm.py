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


def search_depth(mices,holes):
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
        prev_mices_left = node_to_climb['mices']         # save prev mices and holes
        prev_holes_state = node_to_climb['holes']

        for index,mice in enumerate(prev_mices_left):       # run through each mice and hole
            for hole in prev_holes_state:
                current_holes_state = copy.deepcopy(prev_holes_state)
                if len(current_holes_state[hole]) < length_holes[hole]:
                    # once it founds a possible mice and hole, update NODE TO CLIMB and break out of loop
                    current_holes_state[hole].append(mice)
                    current_mices_left = [m for k,m in enumerate(prev_mices_left) if index != k]
                    current_cost = abs(mice - hole)
                    node_to_climb = {"floor": floor, "mices": current_mices_left, "holes": current_holes_state, "cost": current_cost}

                    break
            break


        # increment total_cost
        total_cost += node_to_climb["cost"]
        print "TOTAL COST", total_cost
        print ""
        print "NEW NODE", node_to_climb
        print ""
        print "############"
        print ""
        
    return total_cost

print search_depth(mices,holes)
