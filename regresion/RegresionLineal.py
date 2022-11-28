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

    def regresion_lineal(self, seed=99):
        hora_local = self.Y.columns[1];
        fechas = self.Y.get([hora_local])

        temperatura = self.Y.columns[0];
        self.Y = self.Y.get([temperatura])

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=99)

        # Normalizacion
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled= scaler.transform(X_train)
        X_test_scaled= scaler.transform(X_test)
        X_scaled = scaler.transform(self.X)

        #print(">>>> Usando Ridge")
        clf = Ridge(alpha=0.1).fit(X_train_scaled, y_train)
        #print("Interseccion (b): {}".format(clf.intercept_))
        #print("Pesos (w): {}".format(clf.coef_))
        r2_score = clf.score(X_test_scaled, y_test)
        #print("Score - Ridge: {}".format(r2_score))

        #print(">>>> Usando Kernel Ridge")
        # Polinomio de grado 6
        krr = KernelRidge(alpha=0.1, kernel='polynomial', degree=3)
        krr.fit(X_train_scaled, y_train)
        r3_score = krr.score(X_test_scaled, y_test)
        #print("Score - Ridge Kernel: {}".format(r3_score))


        max_score =  max(r2_score, r3_score)
        Y_pred = krr.predict(X_test_scaled)
        Y_real = y_test
        fechas = fechas.to_numpy().reshape(len (fechas))

        return max_score, Y_pred, Y_real, fechas

    # Devuelve las predicciones del conjunto X y las reales de todo el conjunto
    def regresion_lineal_total(self, seed=99):
        hora_local = self.Y.columns[1];
        fechas = self.Y.get([hora_local])

        temperatura = self.Y.columns[0];
        self.Y = self.Y.get([temperatura])

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=99)

        # Normalizacion
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled= scaler.transform(X_train)
        X_test_scaled= scaler.transform(X_test)
        X_scaled = scaler.transform(self.X)

        #print(">>>> Usando Ridge")
        clf = Ridge(alpha=0.1).fit(X_train_scaled, y_train)
        r2_score = clf.score(X_test_scaled, y_test)
        #print("Score - Ridge: {}".format(r2_score))

        #print(">>>> Usando Kernel Ridge")
        # Polinomio de grado 6
        krr = KernelRidge(alpha=0.1, kernel='polynomial', degree=3)
        krr.fit(X_train_scaled, y_train)
        r3_score = krr.score(X_test_scaled, y_test)
        #print("Score - Ridge Kernel: {}".format(r3_score))

        max_score =  max(r2_score, r3_score)

        Y_pred = krr.predict(X_scaled)
        Y_real = self.Y.values
        fechas = fechas.to_numpy().reshape(len (fechas))

        return max_score, Y_pred, Y_real, fechas
