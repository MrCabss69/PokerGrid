import subprocess as sp
import numpy as np
import pandas as pd
from poker import Hand
from time import time


# Start time
t = time()

# holding hands of respective players: position i are the player i holdings for sims
# , ['AA', 'KK'], ['QQ', 'TT']
hands = [['QTo', 'AKo']]
hands = [[Hand(hands[i][j]) for j in range(len(hands[i]))]
         for i in range(len(hands))]
print(hands,'\n')


# TODO: optimizar la siguiente parte, habría que enfrentar conjuntos de manos no sólo combos individuales
# almacenamos las manos combo por combo enfrentando los rangos al completo
vs_ = []
for vs in hands:
    for c1 in vs[0].to_combos():
        for c2 in vs[1].to_combos():
            vs_.append([str(c1),str(c2)])

print(vs_)
print()

# TODO: mejorar eficiencia de las llamadas a poker-odds -> habría que implementar un proyecto NodeJS
# en él exportar el módulo y hacer las llamadas a la api -- configurar boards, manos a simular, etc.
# A FUTURO: configurar la libreria de python eval7 para calcular las equities de los rangos
 
# recorremos cada enfrentamiento
resultados = {}
for c in vs_:

    cards = []
    for comb in c:

        # recorremos cada mano del enfrentamiento
        aux = str(comb)

        # formateamos el string de la carta para la llamada a poker-odds
        for k, v in {'c': '♣', 'h': '♥', 'd': '♦', 's': '♠'}.items():
            aux = aux.replace(v, k)

        # añadimos la carta formateada
        cards.append(aux)

    # ejecutamos una llamada al módulo externo para el enfrentamiento
    comando = 'poker-odds ' + ' '.join(cards) + ' -i 10000'
    process = sp.Popen(comando.split(), stdout=sp.PIPE)

    # recibimos output y el error de la ejecución
    output, error = process.communicate()

    # decodificamos la respuesta
    text = output.decode('utf-8').split('\n')

    # y la almacenamos en un diccionario de la forma: { mano_1-mano2: [ev_mano_1, ev_mano_2] }
    resultados.update(
        {'-'.join(cards): [float(t[t.index('%')-4:t.index('%')]) for t in text if '%' in t]})


dataframe = pd.DataFrame.from_dict(resultados).T

#print(resultados)
print(dataframe)

print()
print('Tiempo de ejecución: ', time()-t)


""" 

EJECUCIONES: hay 32 enfrentamientos distintos en [['QTs', 'AKs'],['AA', 'KK']] == [[4,4],[4,4]] == 4*4 + 4*4 


# quitar enfrentamientos redundantes y calcular las permutaciones
# lo mismo: calcular que casos son dependientes e independientes entre sí


# permutaciones_posibles * probabilidad individual (abstracción - agrupamos por casos de idénticas probs)
CASO 1: QcTc vs. AcKc == QhTh vs. AhKh == QsTs vs. AsKs == QdTd vs. AdKd 
CASO 2: QdTc vs. AsKh == QcTd vs. AsKh == QcTd vs. AhKs == QdTc vs. AhKs
.
.


para [['QTs', 'AKs'],['AA', 'KK']] y 1000 iteraciones ~ 7.01 segundos
para [['QTs', 'AKs'],['AA', 'KK']] y 5000 iteraciones ~ 9.34 segundos
para [['QTs', 'AKs'],['AA', 'KK']] y -e               ~ 400. segundos

"""
