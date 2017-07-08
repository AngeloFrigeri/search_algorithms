import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# New Antecedent/Consequent objects hold universe variables and membership
# functions
error = ctrl.Antecedent(np.linspace(-100, 100, 3), 'error')
delta = ctrl.Antecedent(np.linspace(-100, 100, 3), 'delta')
output = ctrl.Consequent(np.linspace(0, 100, 5), 'output')

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
"""
error['nb'] = fuzz.trimf(error.universe, [-100, -100, -50])
error['ns'] = fuzz.trimf(error.universe, [-100, -50, 0])
error['ze'] = fuzz.trimf(error.universe, [-50, 0, 50])
error['ps'] = fuzz.trimf(error.universe, [0, 50, 100])
error['pb'] = fuzz.trimf(error.universe, [50, 100, 100])

delta['nb'] = fuzz.trimf(delta.universe, [-100, -100, -50])
delta['ns'] = fuzz.trimf(delta.universe, [-100, -50, 0])
delta['ze'] = fuzz.trimf(delta.universe, [-50, 0, 50])
delta['ps'] = fuzz.trimf(delta.universe, [0, 50, 100])
delta['pb'] = fuzz.trimf(delta.universe, [50, 100, 100])
"""

output['ps'] = fuzz.trimf(output.universe, [0, 50, 100])
output['pb'] = fuzz.trimf(output.universe, [50, 100, 100])
output['ze'] = fuzz.trimf(output.universe, [0, 0, 50])
output['ps'] = fuzz.trimf(output.universe, [0, 50, 100])
output['pb'] = fuzz.trimf(output.universe, [65, 100, 100])

# names = ['nb', 'ns', 'ze', 'ps', 'pb']
names = ['n', 'z', 'p']
error.automf(names=names)
delta.automf(names=names)

# cont = ['ng', 'np', 'ze', 'pp', 'pg']
# output.automf(names=cont)

output.view()


def pause():
	raw_input('oi')

pause()
"""
rule0 = ctrl.Rule(antecedent=((error['nb'] & delta['nb']) |
                              (error['ns'] & delta['nb']) |
                              (error['nb'] & delta['ns'])),
                  consequent=output['nb'], label='rule nb')

rule1 = ctrl.Rule(antecedent=((error['nb'] & delta['ze']) |
                              (error['nb'] & delta['ps']) |
                              (error['ns'] & delta['ns']) |
                              (error['ns'] & delta['ze']) |
                              (error['ze'] & delta['ns']) |
                              (error['ze'] & delta['nb']) |
                              (error['ps'] & delta['nb'])),
                  consequent=output['ns'], label='rule ns')

rule2 = ctrl.Rule(antecedent=((error['nb'] & delta['pb']) |
                              (error['ns'] & delta['ps']) |
                              (error['ze'] & delta['ze']) |
                              (error['ps'] & delta['ns']) |
                              (error['pb'] & delta['nb'])),
                  consequent=output['ze'], label='rule ze')

rule3 = ctrl.Rule(antecedent=((error['ns'] & delta['pb']) |
                              (error['ze'] & delta['pb']) |
                              (error['ze'] & delta['ps']) |
                              (error['ps'] & delta['ps']) |
                              (error['ps'] & delta['ze']) |
                              (error['pb'] & delta['ze']) |
                              (error['pb'] & delta['ns'])),
                  consequent=output['ps'], label='rule ps')

rule4 = ctrl.Rule(antecedent=((error['ps'] & delta['pb']) |
                              (error['pb'] & delta['pb']) |
                              (error['pb'] & delta['ps'])),
                  consequent=output['pb'], label='rule pb')

"""

"""
rule0 = ctrl.Rule(antecedent=((error['z'] & delta['p']) |
                              (error['p'] & delta['z']) |
                              (error['p'] & delta['p'])),
                  consequent=output['n'], label='n')

rule1 = ctrl.Rule(antecedent=((error['n'] & delta['p']) |
                              (error['z'] & delta['z']) |
                              (error['p'] & delta['n'])),
                  consequent=output['z'], label='z')

rule2 = ctrl.Rule(antecedent=((error['n'] & delta['n']) |
                              (error['n'] & delta['z']) |
                              (error['z'] & delta['n'])),
                  consequent=output['p'], label='p')
"""

rule0 = ctrl.Rule(antecedent=(error['n'] & delta['n']),
                  consequent=output['pg'], label='pg')

rule1 = ctrl.Rule(antecedent=((error['n'] & delta['z']) |
                              (error['n'] & delta['p']) |
                              (error['z'] & delta['n'])),
                  consequent=output['pp'], label='pp')

rule2 = ctrl.Rule(antecedent=(error['z'] & delta['z']),
                  consequent=output['ze'], label='ze')

rule3 = ctrl.Rule(antecedent=((error['z'] & delta['p']) |
                              (error['p'] & delta['n']) |
                              (error['p'] & delta['z'])),
                  consequent=output['np'], label='np')

rule4 = ctrl.Rule(antecedent=(error['p'] & delta['p']),
                  consequent=output['ng'], label='ng')

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4])


sim = ctrl.ControlSystemSimulation(system, flush_after_run=21 * 21 + 1)

area_base = 10
referencia = 50
altura_atual = 10
delta = 0
controle_anterior = 0
vazao_saida = 20
ts = 0.1

altura_vec = []
controle_vec = []
tempo = []
error_vec = []
for i in range(200):
	erro_atual = referencia - altura_atual

	sim.input['error'] = erro_atual
	sim.input['delta'] = delta

	sim.compute()

	# delta_vazao_controle = sim.output['output']
	vazao_controle = sim.output['output']
	# vazao_controle = controle_anterior + delta_vazao_controle

	delta = (vazao_controle - controle_anterior)/ts
	controle_anterior = vazao_controle

	altura_atual = altura_atual + (vazao_controle*ts - vazao_saida*ts)/area_base

	altura_vec.append(altura_atual)
	controle_vec.append(vazao_controle)
	error_vec.append(erro_atual)
	tempo.append(i*ts)
	print i


fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(tempo, altura_vec, '-', color="r", linewidth=2.5, alpha=0.7, label='Altura')
ax0.plot(tempo, controle_vec, '-', color="green", linewidth=2.5, alpha=0.7, label='Controle')
ax0.plot(tempo, error_vec, '-', color="b", linewidth=2.5, alpha=0.7, label='Erro')
ax0.legend(loc='upper right', shadow=False, prop={'size': 12})
ax0.set_xlabel('tempo', fontsize=13)
ax0.set_ylabel('saida normalizada', fontsize=13)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#707070')
ax0.xaxis.label.set_color('#707070')
ax0.yaxis.label.set_color('#707070')
ax0.tick_params(axis='x', colors='#707070')
ax0.tick_params(axis='y', colors='#707070')
plt.savefig("fuzzy.png", bbox_inches='tight', pad_inches=0.1)
