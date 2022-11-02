from utilidades.Lector import Lector
from regresion.RegresionLineal import RegresionLineal

if __name__ == '__main__':
    l = Lector('data/encb-90.csv')
    # Toma los registros de las 12hrs y 24hrs de 90 dias desde 2022-10-15 hacia atras
    X,Y = l.get_data('2022-10-15', ['00:00:00', '12:00:00'], 90)
    rl = RegresionLineal(X,Y)
    rl.regresion_lineal()
