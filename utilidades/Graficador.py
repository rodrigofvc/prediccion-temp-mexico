import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
import matplotlib.dates as mdates
import pandas as pd

class Graficador(object):

    def grafica_total(self, fechas, Y_real):
        fechas = Y_real.get(['Hora Local'])
        temperatura = Y_real.columns[0];
        temps = Y_real.get([temperatura])
        #fechas = fechas.to_numpy().reshape(len (fechas))
        figure(figsize=(15, 8))
        print()
        print (fechas.values)
        plt.plot(fechas.values, temps.values, '-o', label='temperatura')
        plt.xlabel("Fecha (YYYY-MM-DD)")
        plt.ylabel("Temperatura (°C)")
        plt.grid()
        plt.gca().tick_params(axis='x')
        #plt.gca().tick_params(axis='x', labelrotation=45)
        plt.legend(loc="upper left")
        plt.title('Temperatura a las 9 AM desde el 17 de Julio hasta el 11 de Noviembre')
        plt.savefig('total-17-29')
        plt.show()

    # Grafica todo el vector X     
    def grafica_fechas(self, fechas, Y_real, Y_pred, hora, fecha_cercana, fecha_lejana):
        #fechas = fechas.to_numpy().reshape(len (fechas))
        figure(figsize=(15, 8))
        plt.plot(fechas, Y_real, '-o', label='y_real')
        plt.plot(fechas, Y_pred, '-o', label='y_pred')
        plt.xlabel("Fecha (YYYY-MM-DD)")
        plt.ylabel("Temperatura (°C)")
        plt.grid()
        plt.gca().tick_params(axis='x')
        #plt.gca().tick_params(axis='x', labelrotation=45)
        plt.legend(loc="upper left")
        plt.title('Temperatura a las {} desde {} hasta {}'.format(hora, fecha_lejana, fecha_cercana))
        plt.show()


    def grafica(self, hora, dias_pasado, dias_futuro, Y_pred, Y_real, mse, rmse, mae, horaEtq, sin_var):
        figure(figsize=(15, 8))

        X = np.arange(1,len(Y_pred)+1,1)
        plt.scatter(X, Y_real.values, label='y_true', color="g")
        plt.scatter(X, Y_pred, label='y_pred', color="blue")
        plt.xlabel("Instancia")
        plt.ylabel("Temperatura (°C)")
        plt.xticks(X)
        plt.grid()
        plt.gca().tick_params(axis='x')
        #plt.gca().tick_params(axis='x', labelrotation=45)
        plt.legend(loc="upper left")
        plt.title('Predicción temperatura {} (info. de {} dias al pasado, pred. de {} dias a futuro) MSE: {:.2f} RMSE: {:.2f} MAE: {:.2f} '.format(hora, dias_pasado, dias_futuro, mse, rmse, mae))
        if sin_var:
            dir_var = 'img/no_var/'
        else:
            dir_var = 'img/var/'
        dir = dir_var + horaEtq[0] + horaEtq[1] + '/'
        nombre = horaEtq[0] + horaEtq[1] + "-" + str(dias_pasado) + "ps-" + str(dias_futuro) + "ft"
        print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DIR {}'.format(dir+nombre))
        #plt.savefig(dir + nombre)
        plt.show()
