from utilidades.Lector import Lector
from regresion.RegresionLineal import RegresionLineal
import sys
import numpy as np

if __name__ == '__main__':
    l = Lector('data/encb-90-2.csv')
    # Mostrar imagenes
    show = False
    # Intentar 100 ejecuciones
    loop = False
    # Estimar sin variables
    sin_variables = True
    # Toma los registros de las 12 hrs y estima la temperatura en ese punto,
    # tomando 5 registros alrededor de esta hora desde 10 dias atras.
    # Z es el valor de los dias en el futuro
    # X_unknow las variables en el futuro
    X, Y, Z, X_unknown = l.get_data('2022-11-01', '09:00:00', n=5, dias=16, show=show, dias_futuro=5)

    # Para estimar sin variables
    if sin_variables:
        X_unknown = np.arange(0, len(Z)).reshape(-1, 1)
        X = np.arange(0, len(Y)).reshape(-1, 1)

    # Datos del futuro para probar
    #print("\n--------> Z \n")
    #print(Z)
    #print("\n--------> X_unknow \n")
    #print(X_unknown)



    #print(X)
    rl = RegresionLineal(X, Y)
    semilla = int(sys.argv[1])
    max_semilla = semilla
    max_score = rl.regresion_lineal(semilla, show, Z, X_unknown)
    if loop:
        for i in range(0,100,1):
            score = rl.regresion_lineal(i, show, Z, X_unknown)
            if score > max_score:
                max_score = score
                max_semilla = i
    """
        Resultados sin variables
        '2022-11-01', '09:00:00' n=5, dias=16, show=show, dias_futuro=1 19
        '2022-11-01', '09:00:00' n=5, dias=15, show=show, dias_futuro=3 17
    """
    print("MAX --> SEMILLA: {} SCORE: {}".format(max_semilla, max_score))
