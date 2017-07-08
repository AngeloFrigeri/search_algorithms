# Libraries Included:
# Numpy, Scipy, Scikit, Pandas
import matplotlib.pyplot as plt
import copy
import numpy.random as nprnd
import datetime
from numpy import median
from random import randint

import itertools
mices = [6, 2, 8, 9]
holes = [(3,6),(2,1),(3,6),(4,7),(4,7)]
# mices = [10, 20, 30, 40, 50, 45, 35]
# holes = [(-1000000000, 10), (1000000000, 1)]


def clean_hole(holes):
	length_holes = dict()

	for j, c in holes:
		if j in list(length_holes.keys()):
			length_holes[j] += c
		else:
			length_holes[j] = c
	return length_holes


def menor_custo_min(list_of_dicts):
	menor = list_of_dicts[0]
	quantidade = len(list_of_dicts)
	if quantidade > 1:
		for i in range(quantidade):
			item = list_of_dicts[i]['cost']
			if item + h_min(list_of_dicts[i]) < menor['cost'] + h_min(menor):
				menor = list_of_dicts[i]
	return menor

def menor_custo_aver(list_of_dicts):
	menor = list_of_dicts[0]
	quantidade = len(list_of_dicts)
	if quantidade > 1:
		for i in range(quantidade):
			item = list_of_dicts[i]['cost']
			if item + h_aver(list_of_dicts[i]) < menor['cost'] + h_aver(menor):
				menor = list_of_dicts[i]
	return menor

def menor_custo_median(list_of_dicts):
	menor = list_of_dicts[0]
	quantidade = len(list_of_dicts)
	if quantidade > 1:
		for i in range(quantidade):
			item = list_of_dicts[i]['cost']
			if item + h_median(list_of_dicts[i]) < menor['cost'] + h_median(menor):
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


def search_min(mices, holes):
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
		filhos = abrir(no_de_menor_custo, length_holes)
		abertos += filhos
		nodes_percorridos += len(filhos)
		no_de_menor_custo = menor_custo_min(abertos)
		if no_de_menor_custo['mices'] == []:
			return no_de_menor_custo["cost"], nodes_percorridos

def search_aver(mices, holes):
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
		filhos = abrir(no_de_menor_custo, length_holes)
		abertos += filhos
		nodes_percorridos += len(filhos)
		no_de_menor_custo = menor_custo_aver(abertos)
		if no_de_menor_custo['mices'] == []:
			return no_de_menor_custo["cost"], nodes_percorridos

def search_median(mices, holes):
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
		filhos = abrir(no_de_menor_custo, length_holes)
		abertos += filhos
		nodes_percorridos += len(filhos)
		no_de_menor_custo = menor_custo_median(abertos)
		if no_de_menor_custo['mices'] == []:
			return no_de_menor_custo["cost"], nodes_percorridos

######### MAIN ###############
total_time = {"Minima": [],
              "Media": [],
              "Mediana": []}
nodes = {"Minima": [],
              "Media": [],
              "Mediana": []}
cost = {"Minima": [],
              "Media": [],
              "Mediana": []}
# inputs
iterations = 6
mices_v = [6, 2, 4, 1, 1, 9]
holes_v = [(3, 6), (2, 1), (5, 7), (2, 9), (2, 5), (6, 8)]
size=[]
for i in range(2, iterations+1):
	mices = mices_v[0: i]
	holes = holes_v[0: i]
	size.append(len(mices))
	print mices
	print holes
	print i
	print "a *"
	ti = datetime.datetime.now()
	custo_total, nodes_percorridos = search_min(mices, holes)
	t_A = (datetime.datetime.now() - ti).total_seconds()
	total_time["Minima"].append(t_A)
	nodes["Minima"].append(nodes_percorridos)
	cost["Minima"].append(custo_total)

	ti = datetime.datetime.now()
	custo_total, nodes_percorridos = search_aver(mices, holes)
	t_A = (datetime.datetime.now() - ti).total_seconds()
	total_time["Media"].append(t_A)
	nodes["Media"].append(nodes_percorridos)
	cost["Media"].append(custo_total)

	ti = datetime.datetime.now()
	custo_total, nodes_percorridos = search_median(mices, holes)
	t_A = (datetime.datetime.now() - ti).total_seconds()
	total_time["Mediana"].append(t_A)
	nodes["Mediana"].append(nodes_percorridos)
	cost["Mediana"].append(custo_total)

	mices.append(randint(0, 10))
	holes.append((randint(0, 10), randint(0, 10)))

fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(size, [time for time in total_time["Minima"]], '-', color="b", linewidth=2.5, alpha=0.7,
         label='Minima')
ax0.plot(size, [time for time in total_time["Media"]], '-', color="r", linewidth=2.5, alpha=0.7,
         label='Media')
ax0.plot(size, [time for time in total_time["Mediana"]], '-', color="green", linewidth=2.5, alpha=0.7,
         label='Mediana')
ax0.legend(loc='upper right', shadow=False, prop={'size': 12})
ax0.set_xlabel('Numero de ratos e buracos', fontsize=13)
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
ax0.plot(size, [time for time in nodes["Minima"]], '-', color="b", linewidth=2.5, alpha=0.7,
         label='Minima')
ax0.plot(size, [time for time in nodes["Media"]], '-', color="r", linewidth=2.5, alpha=0.7,
         label='Media')
ax0.plot(size, [time for time in nodes["Mediana"]], '-', color="green", linewidth=2.5, alpha=0.7,
         label='Mediana')
ax0.legend(loc='upper right', shadow=False, prop={'size': 12})
ax0.set_xlabel('Numero de ratos e buracos', fontsize=13)
ax0.set_ylabel('Nos percorridos', fontsize=13)
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
ax0.plot(size, [time for time in cost["Minima"]], '-', color="b", linewidth=2.5, alpha=0.7,
         label='Minima')
ax0.plot(size, [time for time in cost["Media"]], '-', color="r", linewidth=2.5, alpha=0.7,
         label='Media')
ax0.plot(size, [time for time in cost["Mediana"]], '-', color="green", linewidth=2.5, alpha=0.7,
         label='Mediana')
ax0.legend(loc='upper right', shadow=False, prop={'size': 12})
ax0.set_xlabel('Numero de ratos e buracos', fontsize=13)
ax0.set_ylabel('Distancia total', fontsize=13)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#707070')
ax0.xaxis.label.set_color('#707070')
ax0.yaxis.label.set_color('#707070')
ax0.tick_params(axis='x', colors='#707070')
ax0.tick_params(axis='y', colors='#707070')
plt.savefig("distance.png", bbox_inches='tight', pad_inches=0.1)
