# -*- coding: utf-8 -*-

# Libraries Included:
# Numpy, Scipy, Scikit, Pandas
import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy.random as nprnd
import datetime

# inputs
iterations = 6
# mices = [6, 2, 8, 9]
# holes = [(3,6),(2,1),(3,6),(4,7),(4,7)]
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

########## BUSCA CEGA ##########

def search_depth(mices,holes):
    length_holes = clean_hole(holes)
    keys = ('floor','mices','holes','cost')

    mices_left = mices
    holes_state = {}
    for hole,_ in holes:
        holes_state.setdefault(hole,[])

    node_to_climb = {"floor": 0, "mices": mices_left, "holes": holes_state, "cost": 0}
    total_cost = 0
    nodes_percorridos = 1
    for floor in range(1,1+len(mices)):
        # print "FLOOR", floor
        # print ""
        # print "CURRENT NODE", node_to_climb
        # print ""
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
                    nodes_percorridos += 1
                    # print nodes_percorridos
                    break
            break


        # increment total_cost
        total_cost += node_to_climb["cost"]
        # print "TOTAL COST", total_cost
        # print ""
        # print "NEW NODE", node_to_climb
        # print ""
        # print "############"
        # print ""
    return total_cost, nodes_percorridos


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
    nodes_percorridos = 1
    nodo_zero = {"mices": mices_left, "holes": holes_state, "cost": 0}
    abertos.append(nodo_zero)
    no_de_menor_custo = nodo_zero
    while len(abertos) != 0:
        abertos.remove(no_de_menor_custo)
    	filhos = abrir(no_de_menor_custo, length_holes)
        nodes_percorridos += len(filhos)
        abertos += filhos
    	no_de_menor_custo = menor_custo(abertos)
    	if no_de_menor_custo['mices'] == []:
    		return no_de_menor_custo, nodes_percorridos



########## BUSCA INTELIGENTE ##########

def search_subida_montanha(mices,holes):
    length_holes = clean_hole(holes)
    keys = ('floor','mices','holes','cost')

    mices_left = mices
    holes_state = {}
    for hole,_ in holes:
        holes_state.setdefault(hole,[])

    node_to_climb = {"floor": 0, "mices": mices_left, "holes": holes_state, "cost": 0}
    total_cost = 0
    nodes_percorridos = 1
    for floor in range(1,1+len(mices)):
        # print "FLOOR", floor
        # print ""
        # print "CURRENT NODE", node_to_climb
        # print ""
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
                    nodes_percorridos += 1
        # sort list_of_nodes_in_floor by cost
        sorted_nodes_in_floor = sorted(list_of_nodes_in_floor, key = lambda node: node['cost'])
        # print "SORTED NODES IN FLOOR", sorted_nodes_in_floor
        # print ""
        # # picks the next node by the lower cost
        # node_to_climb = sorted_nodes_in_floor[0]
        # print "NEW NODE TO CLIMB", node_to_climb
        # print ""
        # # increment total_cost
        # total_cost += node_to_climb["cost"]
        # print "TOTAL COST", total_cost
        # print ""
        # print "############"
        # print ""

    return total_cost, nodes_percorridos


def menor_custo_A(list_of_dicts, length_holes):
	menor = list_of_dicts[0]
	quantidade = len(list_of_dicts)
	if quantidade > 1:
		for i in range(quantidade):
			item = list_of_dicts[i]['cost']
			if item + h_min(list_of_dicts[i]) < menor['cost'] + h_min(menor):
				menor = list_of_dicts[i]
	return menor



def h_guloso(node, length_holes):
	mices = copy.deepcopy(node['mices'])
	holes_state = copy.deepcopy(node['holes'])
	#combinacao = [zip(x, list(holes_state.keys())) for x in itertools.permutations(mices, len(holes_state))]
	combinacao = [(mices[i], list(holes_state.keys())[j]) for i in xrange(len(mices)) for j in xrange(len(list(holes_state.keys())))]
	cost = []
	for comb in combinacao:
		esta_cheio = False
		cost_to_append = 0
		temp_holes_state = copy.deepcopy(holes_state)
		for tuple in comb:
			cost_to_append += abs(tuple[0]-tuple[1])
			temp_holes_state[tuple[1]].append(tuple[0])
			if len(temp_holes_state[tuple[1]]) >= length_holes[tuple[1]]:
				esta_cheio = True
		if esta_cheio == False:
			cost.append(cost_to_append)
	return min(cost)

def h_median(node):
	mices = copy.deepcopy(node['mices'])
	holes_state = copy.deepcopy(node['holes'])
	cost = []
	for hole in holes_state:
		cost_to_append = 0
		for mice in mices:
			cost_to_append += abs(mice-hole)
		cost.append(cost_to_append)
	return median(cost)


def h_min(node):
	mices = copy.deepcopy(node['mices'])
	holes_state = copy.deepcopy(node['holes'])
	cost = []
	for hole in holes_state:
		cost_to_append = 0
		for mice in mices:
			cost_to_append += abs(mice-hole)
		cost.append(cost_to_append)
	return min(cost)


def h_aver(node):
	mices = copy.deepcopy(node['mices'])
	holes_state = copy.deepcopy(node['holes'])
	cost = []
	for hole in holes_state:
		cost_to_append = 0
		for mice in mices:
			cost_to_append += abs(mice-hole)
		cost.append(cost_to_append)
	return sum(cost)/float(len(cost))

def abrir_A(node, length_holes):
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


def search_A(mices, holes):
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
    nodes_percorridos = 1
    while len(abertos) != 0:
        abertos.remove(no_de_menor_custo)
        filhos = abrir_A(no_de_menor_custo, length_holes)
        nodes_percorridos += len(filhos)
        abertos += filhos
        no_de_menor_custo = menor_custo_A(abertos, length_holes)
        if no_de_menor_custo['mices'] == []:
            return no_de_menor_custo, nodes_percorridos


######### MAIN ###############
total_time = {  "profundidade": [],
                "largura": [],
                "montanha": [],
                "a_*": []}
nodes = {  "profundidade": [],
                "largura": [],
                "montanha": [],
                "a_*": []}
cost = {  "profundidade": [],
                "largura": [],
                "montanha": [],
                "a_*": []}

for i in range(1,iterations):
    print i
    mices = list(nprnd.randint(100, size=12*i))
    holes_positions = list(nprnd.randint(100, size=12*i))
    holes_size = list(nprnd.randint(100, size=12*i))
    holes = zip(holes_positions,holes_size)

    ti = datetime.datetime.now()
    custo_total, nodes_percorridos = search_depth(mices,holes)
    t_depth = (datetime.datetime.now() - ti).total_seconds
    total_time["profundidade"].append(t_depth)
    nodes["profundidade"].append(nodes_percorridos)
    cost["profundidade"].append(cost)

    ti = datetime.datetime.now()
    custo_total, nodes_percorridos = search(mices,holes)
    t_largura = (datetime.datetime.now() - ti).total_seconds
    total_time["largura"].append(t_largura)
    nodes["largura"].append(nodes_percorridos)
    cost["largura"].append(cost)

    ti = datetime.datetime.now()
    custo_total, nodes_percorridos = search_subida_montanha(mices,holes)
    t_sm = (datetime.datetime.now() - ti).total_seconds
    total_time["montanha"].append(t_sm)
    nodes["montanha"].append(nodes_percorridos)
    cost["montanha"].append(cost)

    ti = datetime.datetime.now()
    custo_total, nodes_percorridos = search_A(mices,holes)
    t_A = (datetime.datetime.now() - ti).total_seconds
    total_time["a_*"].append(t_A)
    nodes["a_*"].append(nodes_percorridos)
    cost["a_*"].append(cost)

fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(range(1,iterations), [time for time in total_time["profundidade"]], '-', color="#707070", linewidth=2.5, alpha = 0.7, label='Profundidade')
ax0.plot(range(1,iterations), [time for time in total_time["largura"]], '-', color="b", linewidth=2.5, alpha = 0.7, label='Largura')
ax0.plot(range(1,iterations), [time for time in total_time["montanha"]], '-', color="r", linewidth=2.5, alpha = 0.7, label='Subida da Montanha')
ax0.plot(range(1,iterations), [time for time in total_time["a_*"]], '-', color="green", linewidth=2.5, alpha = 0.7, label='A*')
ax0.legend(loc='upper right', shadow=False, prop={'size':12})
ax0.set_xlabel('Número de ratos (em dezenas)', fontsize=13)
ax0.set_ylabel('Tempo', fontsize=13)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#707070')
ax0.xaxis.label.set_color('#707070')
ax0.yaxis.label.set_color('#707070')
ax0.tick_params(axis='x', colors='#707070')
ax0.tick_params(axis='y', colors='#707070')
plt.savefig("tempo.png", bbox_inches='tight', pad_inches=0.1)

fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(range(1,iterations), [time for time in nodes["profundidade"]], '-', color="#707070", linewidth=2.5, alpha = 0.7, label='Profundidade')
ax0.plot(range(1,iterations), [time for time in nodes["largura"]], '-', color="b", linewidth=2.5, alpha = 0.7, label='Largura')
ax0.plot(range(1,iterations), [time for time in nodes["montanha"]], '-', color="r", linewidth=2.5, alpha = 0.7, label='Subida da Montanha')
ax0.plot(range(1,iterations), [time for time in nodes["a_*"]], '-', color="green", linewidth=2.5, alpha = 0.7, label='A*')
ax0.legend(loc='upper right', shadow=False, prop={'size':12})
ax0.set_xlabel('Número de ratos (em dezenas)', fontsize=13)
ax0.set_ylabel('Nós percorridos', fontsize=13)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#707070')
ax0.xaxis.label.set_color('#707070')
ax0.yaxis.label.set_color('#707070')
ax0.tick_params(axis='x', colors='#707070')
ax0.tick_params(axis='y', colors='#707070')
plt.savefig("nodes.png", bbox_inches='tight', pad_inches=0.1)

fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(range(1,iterations), [time for time in cost["profundidade"]], '-', color="#707070", linewidth=2.5, alpha = 0.7, label='Profundidade')
ax0.plot(range(1,iterations), [time for time in cost["largura"]], '-', color="b", linewidth=2.5, alpha = 0.7, label='Largura')
ax0.plot(range(1,iterations), [time for time in cost["montanha"]], '-', color="r", linewidth=2.5, alpha = 0.7, label='Subida da Montanha')
ax0.plot(range(1,iterations), [time for time in cost["a_*"]], '-', color="green", linewidth=2.5, alpha = 0.7, label='A*')
ax0.legend(loc='upper right', shadow=False, prop={'size':12})
ax0.set_xlabel('Número de ratos (em dezenas)', fontsize=13)
ax0.set_ylabel('Distância total', fontsize=13)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#707070')
ax0.xaxis.label.set_color('#707070')
ax0.yaxis.label.set_color('#707070')
ax0.tick_params(axis='x', colors='#707070')
ax0.tick_params(axis='y', colors='#707070')
plt.savefig("distance.png", bbox_inches='tight', pad_inches=0.1)
