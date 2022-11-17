from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
from sklearn.kernel_ridge import KernelRidge

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd


class RegresionLineal(object):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def regresion_lineal(self, seed, show):
        hora_local = self.Y.columns[1];
        fechas = self.Y.get([hora_local])

        temperatura = self.Y.columns[0];
        self.Y = self.Y.get([temperatura])

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=seed)

        """
        print(">>>> Usando regresion lineal")
        linreg= LinearRegression().fit(X_train, y_train)
        print("Interseccion (b): {}".format(linreg.intercept_))
        print("Pesos (w): {}".format(linreg.coef_))
        r1_score = linreg.score(X_test, y_test)
        print("Score - RegresionLineal: {}".format(r1_score))
        """


        # Normalizacion
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled= scaler.transform(X_train)
        X_test_scaled= scaler.transform(X_test)
        X_scaled = scaler.transform(self.X)

        """
        print(">>>> Usando Ridge")
        clf = Ridge(alpha=0.1).fit(X_train_scaled, y_train)
        print("Interseccion (b): {}".format(clf.intercept_))
        print("Pesos (w): {}".format(clf.coef_))
        r2_score = clf.score(X_test_scaled, y_test)
        print("Score - Ridge: {}".format(r2_score))
        """

        #print(">>>> Usando Kernel Ridge")
        # Polinomio de grado 6
        krr = KernelRidge(alpha=0.1, kernel='polynomial', degree=6)
        krr.fit(X_train_scaled, y_train)
        r3_score = krr.score(X_test_scaled, y_test)
        #print("Score - Ridge Kernel: {}".format(r3_score))

        """
        fig, axs = plt.subplots(2, 2)
        # Regresion lineal
        axs[0,0].plot(y_test.values, '-o', label='test')
        axs[0,0].plot(linreg.predict(X_test), '-o', label='prediccion')
        axs[0,0].legend(loc="upper left")
        axs[0,0].set_title('Regresion lineal simple   score:{:.6f}'.format(r1_score))
        # Regresion Ridge
        axs[0,1].plot(y_test.values, '-o', label='test')
        axs[0,1].plot(clf.predict(X_test_scaled), '-o', label='prediccion')
        axs[0,1].legend(loc="upper left")
        axs[0,1].set_title('Regresion Ridge  score:{:.6f}'.format(r2_score))
        # Regresion Kernel Ridge con polinomio 6
        axs[1,0].plot(y_test.values, '-o', label='test')
        axs[1,0].plot(krr.predict(X_test_scaled), '-o', label='prediccion')
        axs[1,0].legend(loc="upper left")
        axs[1,0].set_title('Regresion Kernel Ridge  score:{:.6f}'.format(r3_score))
        """

        plt.plot(fechas.to_numpy().reshape(len (fechas)), self.Y.values, '-o', label='y_test')
        plt.plot(fechas.to_numpy().reshape(len (fechas)), krr.predict(X_scaled), '-o', label='y_pred')
        plt.xlabel("Fecha (YYYY-MM-DD)")
        plt.ylabel("Temperatura (°C)")
        plt.grid()
        plt.gca().tick_params(axis='x', labelrotation=45)
        plt.legend(loc="upper left")
        plt.title('Prediccion temperatura 9 a.m. (dias a futuro)')
        print(r3_score)
        if show:
            plt.show()

        return r3_score
