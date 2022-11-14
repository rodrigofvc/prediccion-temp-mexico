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

    def regresion_lineal(self, semilla, show, Z, X_unknown):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=semilla)

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
        X_scaled = scaler.transform(self.X)
        X_unknown_scaled = scaler.transform(X_unknown)
        X_test_scaled= scaler.transform(X_test)

        print(">>>> Usando Ridge")
        clf = Ridge(alpha=0.1, random_state=semilla).fit(X_train_scaled, y_train)
        print("Interseccion (b): {}".format(clf.intercept_))
        print("Pesos (w): {}".format(clf.coef_))
        r2_score = clf.score(X_test_scaled, y_test)
        print("Score - Ridge: {}".format(r2_score))

        print(">>>> Usando Kernel Ridge")
        # Polinomio de grado 6
        krr = KernelRidge(alpha=0.1, kernel='polynomial', degree=5)
        krr.fit(X_train_scaled, y_train)
        r3_score = krr.score(X_test_scaled, y_test)
        print("Score - Ridge Kernel: {}".format(r3_score))
        print(X_test_scaled)
        print(y_test)

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
        axs[1,0].plot(self.Y.values, '-o', label='test')
        axs[1,0].plot(krr.predict(X_scaled), '-o', label='prediccion')
        axs[1,0].legend(loc="lower left")
        axs[1,0].set_title('Regresion Ridge  score:{:.6f}'.format(r3_score))

        # Muestra la grafica con las predicciones de dias futuros
        fig1 = plt.figure()
        axs1 = fig1.add_subplot(1, 1, 1)
        axs1.set_ylabel("Temperatura")
        axs1.plot(Z.values, '-o', label='test')
        axs1.plot(krr.predict(X_unknown_scaled), '-o', label='prediccion')
        axs1.legend(loc="lower left")
        axs1.set_title('Prediccion a futuro')
        fig1.savefig('kr-pred.png')

        # Muestra la gráfica con toda la informacion
        fig2 = plt.figure()
        axs2 = fig2.add_subplot(1, 1, 1)
        axs2.plot(self.Y.values, '-o', label='test')
        axs2.plot(krr.predict(X_scaled), '-o', label='prediccion')
        axs2.legend(loc="lower left")
        axs2.set_title('Regresion Ridge          score:{:.6f}'.format(r3_score))
        fig2.savefig('kr-total.png')


        #print("SCORE")
        #print(krr.score(X_unknown_scaled, Z.values))
        #print("Z {} \n  X {}".format(Z.values, krr.predict(X_unknown_scaled)))

        if show:
            plt.show()

        max_score = r1_score
        if r2_score > max_score:
            max_score = r2_score
        if r3_score > max_score:
            max_score = r3_score
        return max_score
