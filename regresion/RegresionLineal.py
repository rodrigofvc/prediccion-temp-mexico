from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
from sklearn.kernel_ridge import KernelRidge

import matplotlib.pyplot as plt
import numpy as np


class RegresionLineal(object):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def regresion_lineal(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=0)

        print(">>>> Usando regresion lineal")
        linreg= LinearRegression().fit(X_train, y_train)
        print("Interseccion (b): {}".format(linreg.intercept_))
        print("Pesos (w): {}".format(linreg.coef_))
        r1_score = linreg.score(X_test, y_test)
        print("Score - RegresionLineal: {}".format(r1_score))

        # Normalizacion
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled= scaler.transform(X_train)
        X_test_scaled= scaler.transform(X_test)

        print(">>>> Usando Ridge")
        clf = Ridge(alpha=1.0).fit(X_train_scaled, y_train)
        print("Interseccion (b): {}".format(clf.intercept_))
        print("Pesos (w): {}".format(clf.coef_))
        r2_score = clf.score(X_test_scaled, y_test)
        print("Score - Ridge: {}".format(r2_score))

        print(">>>> Usando Kernel Ridge")
        # Polinomio de grado 6
        krr = KernelRidge(alpha=1.0, kernel='polynomial', degree=6)
        krr.fit(X_train_scaled, y_train)
        r3_score = krr.score(X_test_scaled, y_test)
        print("Score - Ridge Kernel: {}".format(r3_score))

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

        plt.show()
