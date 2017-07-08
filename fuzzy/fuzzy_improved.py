import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# New Antecedent/Consequent objects hold universe variables and membership
# functions
error = ctrl.Antecedent(np.linspace(-100, 100, 51), 'error')
delta = ctrl.Antecedent(np.linspace(-10, 10, 7), 'delta')
output = ctrl.Consequent(np.linspace(-5, 5, 7), 'output')

names = ['ng', 'nm', 'np', 'ze', 'pp', 'pm', 'pg']
# error.automf(names=names)
delta.automf(names=names)
output.automf(names=names)

error['ng'] = fuzz.trimf(error.universe, [-100, -100, -44])
error['nm'] = fuzz.trimf(error.universe, [-68, -44, -20])
error['np'] = fuzz.trimf(error.universe, [-36, -20, 0])
error['ze'] = fuzz.trimf(error.universe, [-4, 0, 4])
error['pp'] = fuzz.trimf(error.universe, [0, 20, 36])
error['pm'] = fuzz.trimf(error.universe, [20, 44, 68])
error['pg'] = fuzz.trimf(error.universe, [44, 100, 100])

rule0 = ctrl.Rule(antecedent=((error['ng'] & delta['pp']) |
                              (error['ng'] & delta['pm']) |
                              (error['ng'] & delta['pg'])),
                  consequent=output['ng'], label='output ng')

rule1 = ctrl.Rule(antecedent=((error['nm'] & delta['pp']) |
                              (error['nm'] & delta['pm']) |
                              (error['nm'] & delta['pg']) |
                              (error['pp'] & delta['ng'])),
                  consequent=output['nm'], label='output nm')

rule2 = ctrl.Rule(antecedent=((error['ng'] & delta['ze']) |
                              (error['nm'] & delta['ze']) |
                              (error['np'] & delta['ze']) |
                              (error['np'] & delta['pp']) |
                              (error['np'] & delta['pm']) |
                              (error['np'] & delta['pg']) |
                              (error['pg'] & delta['ng']) |
                              (error['pg'] & delta['nm']) |
                              (error['pm'] & delta['pg']) |
                              (error['pm'] & delta['nm']) |
                              (error['pp'] & delta['nm'])),
                  consequent=output['np'], label='output np')

rule3 = ctrl.Rule(antecedent=((error['ng'] & delta['np']) |
                              (error['nm'] & delta['np']) |
                              (error['np'] & delta['np']) |
                              (error['pg'] & delta['np']) |
                              (error['pm'] & delta['np']) |
                              (error['pp'] & delta['np']) |
                              (error['ze'] & delta['ng']) |
                              (error['ze'] & delta['nm']) |
                              (error['ze'] & delta['np']) |
                              (error['ze'] & delta['ze']) |
                              (error['ze'] & delta['pp']) |
                              (error['ze'] & delta['pm']) |
                              (error['ze'] & delta['pg'])),
                  consequent=output['ze'], label='output ze')

rule4 = ctrl.Rule(antecedent=((error['ng'] & delta['ng']) |
                              (error['ng'] & delta['nm']) |
                              (error['nm'] & delta['nm']) |
                              (error['np'] & delta['nm']) |
                              (error['pg'] & delta['ze']) |
                              (error['pg'] & delta['pp']) |
                              (error['pm'] & delta['ze']) |
                              (error['pm'] & delta['pp']) |
                              (error['pp'] & delta['ze']) |
                              (error['pp'] & delta['pp']) |
                              (error['pp'] & delta['pm']) |
                              (error['pp'] & delta['pg'])),
                  consequent=output['pp'], label='output pp')

rule5 = ctrl.Rule(antecedent=((error['nm'] & delta['ng']) |
                              (error['np'] & delta['ng']) |
                              (error['pg'] & delta['pm']) |
                              (error['pm'] & delta['pm']) |
                              (error['pm'] & delta['pg'])),
                  consequent=output['pm'], label='output pm')

rule6 = ctrl.Rule(antecedent=(error['pg'] & delta['pg']),
                  consequent=output['pg'], label='output pg')

system = ctrl.ControlSystem(rules=[rule0, rule1, rule2, rule3, rule4, rule5, rule6])


sim = ctrl.ControlSystemSimulation(system, flush_after_run=21 * 21 + 1)

area_base = 10
referencia = 70
altura_atual = 0
delta_erro = 0
erro_anterior = 0
controle_anterior = 0
vazao_saida = 1
ts = 2

altura_vec = []
controle_vec = []
tempo = []
error_vec = []
delta_vec = []
altura_vec = []
controle_vec = []
tempo = []
error_vec = []
delta_vec = []

ITER = 3000/(2*ts)
for i in range(ITER):
	erro_atual = referencia - altura_atual

	sim.input['error'] = erro_atual
	sim.input['delta'] = delta_erro

	sim.compute()

	delta_vazao_controle = sim.output['output']
	# vazao_controle = sim.output['output']
	vazao_controle = controle_anterior + delta_vazao_controle
	if vazao_controle > 100:
		vazao_controle = 100
	elif vazao_controle < 0:
		vazao_controle = 0

	delta_erro = erro_atual - erro_anterior
	erro_anterior = erro_atual
	controle_anterior = vazao_controle

	altura_atual = altura_atual + (vazao_controle * ts - vazao_saida * ts) / area_base
	if altura_atual > 100:
		altura_atual = 100
	elif altura_atual < 0:
		altura_atual = 0

	if i == int(ITER/2):
		referencia = referencia/2

	altura_vec.append(altura_atual)
	controle_vec.append(vazao_controle)
	error_vec.append(erro_atual)
	tempo.append(i * ts)
	delta_vec.append(delta_erro)
	print i

fig1 = plt.figure()
ax0 = fig1.add_subplot(111)
ax0.plot(tempo, altura_vec, '-', color="r", linewidth=2.5, alpha=0.7, label='Altura')
ax0.plot(tempo, controle_vec, '-', color="green", linewidth=2.5, alpha=0.7, label='Controle')
ax0.plot(tempo, error_vec, '-', color="b", linewidth=2.5, alpha=0.7, label='Erro')
ax0.plot(tempo, delta_vec, '-', color="y", linewidth=2.5, alpha=0.7, label='Delta')
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
plt.savefig("fuzzy_imp.png", bbox_inches='tight', pad_inches=0.1)
