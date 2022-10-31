from utilidades.Lector import Lector
from regresion.RegresionLineal import RegresionLineal

if __name__ == '__main__':
    l = Lector('data/encb-90.csv')
    X,Y = l.get_data()
    rl = RegresionLineal(X,Y)
    rl.regresion_lineal()
