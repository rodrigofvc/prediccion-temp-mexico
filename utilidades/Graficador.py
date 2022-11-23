import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd

class Graficador(object):

    def grafica(self, hora, dias_pasado, dias_futuro, score, Y_pred, Y_real, fechas):
        plt.plot(fechas, Y_real, '-o', label='y_test')
        plt.plot(fechas, Y_pred, '-o', label='y_pred')
        plt.xlabel("Fecha (YYYY-MM-DD)")
        plt.ylabel("Temperatura (°C)")
        plt.grid()
        plt.gca().tick_params(axis='x', labelrotation=45)
        plt.legend(loc="upper left")
        plt.title('Predicción temperatura {} ( {} dias a futuro, usando {} dias al pasado ) '.format(hora, dias_futuro, dias_pasado))
        plt.show()
