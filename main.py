from utilidades.Lector import Lector
from regresion.RegresionLineal import RegresionLineal
import sys

if __name__ == '__main__':
    l = Lector('data/encb-90.csv')
    # Toma los registros de las 12 hrs y estima la temperatura en ese punto,
    # tomando 5 registros alrededor de esta hora desde 10 dias atras.
    show = True
    X,Y = l.get_data('2022-10-15', '12:00:00', n=5, dias=10, show=show)
    rl = RegresionLineal(X, Y)
    semilla = int(sys.argv[1])
    max_semilla = semilla
    max_score = rl.regresion_lineal(semilla, show)
    """
    Probar multiples semillas
    for i in range(1,90,1):
        # semilla 30 '2022-10-15' '12:00:00' n=5 dias=10
        # semilla 41 '2022-10-15' '12:00:00' n=5 dias=10
        score = rl.regresion_lineal(i, show)
        if score > max_score:
            max_score = score
            max_semilla = i
    """
    print("MAX --> SEMILLA: {} SCORE: {}".format(max_semilla, max_score))
