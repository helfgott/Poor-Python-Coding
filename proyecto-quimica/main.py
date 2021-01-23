#!/usr/bin/env python3

import sys

elementos = sys.argv[1]

compuestos={
            'co2': 'dioxido de carbono',
            'h2o': 'agua'
            }

def compuesto_quimico(elementos):
    """
    Esta funcion se ocupa de decirme que obtengo de la mezcla de elementos
    """

    # Si el elemento esta en el diccionario imprime el compuesto
    if elementos in compuestos:
        print(compuestos[elementos])
    else:
        print('no se que es')
   
    #print( compuestos = compuestos.get(elementos),'no' )

compuesto_quimico(elementos)
