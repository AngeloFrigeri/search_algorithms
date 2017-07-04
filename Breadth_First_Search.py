# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import copy

#mices = [6, 2, 8, 9]
#holes = [(3,6),(2,1),(3,6),(4,7),(4,7)]
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


def menor_custo(list_of_dicts):
	menor = list_of_dicts[0]
	quantidade = len(list_of_dicts)
	if quantidade > 1:
		for i in range(quantidade-1):
			if list_of_dicts[i]['cost'] < list_of_dicts[i+1]['cost']:
				menor = list_of_dicts[i]
			else:
				menor = list_of_dicts[i+1]
	return menor


def abrir(node, length_holes):
	prev_mices_left = node['mices']
	prev_holes_state = node['holes']
	prev_cost = node['cost']
	children = []
	for index, mice in enumerate(prev_mices_left):
		for hole in prev_holes_state:
			current_holes_state = copy.deepcopy(prev_holes_state)
			if len(current_holes_state[hole]) < length_holes[hole]:
				current_holes_state[hole].append(mice)
				current_mices_left = [m for k, m in enumerate(prev_mices_left) if index != k]
				current_cost = prev_cost + abs(mice - hole)
				dict_to_append = {"mices": current_mices_left, "holes": current_holes_state,
				                  "cost": current_cost}
				children.append(dict_to_append)
	return children


def search(mices, holes):
    abertos = []
    length_holes = clean_hole(holes)
    keys = ('mices', 'holes', 'cost')

    mices_left = mices
    holes_state = {}
    for hole, _ in holes:
        holes_state.setdefault(hole, [])

    nodo_zero = {"mices": mices_left, "holes": holes_state, "cost": 0}
    abertos.append(nodo_zero)
    no_de_menor_custo = nodo_zero
    while len(abertos) != 0:
		abertos.remove(no_de_menor_custo)
		filhos = abrir(no_de_menor_custo, length_holes)
		abertos += filhos
		no_de_menor_custo = menor_custo(abertos)
		if no_de_menor_custo['mices'] == []:
			return no_de_menor_custo

print search(mices, holes)