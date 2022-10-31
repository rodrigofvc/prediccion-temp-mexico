from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge

class RegresionLineal(object):

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def regresion_lineal(self):
        print(">>>> Usando regresion lineal")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, random_state=0)
        linreg= LinearRegression().fit(X_train, y_train)
        print("Interseccion (b): {}".format(linreg.intercept_))
        print("Pesos (w): {}".format(linreg.coef_))
        r1_score = linreg.score(X_test, y_test)
        print("Score - RegresionLineal: {}".format(r1_score))

        print(">>>> Usando Ridge")
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled= scaler.transform(X_train)
        X_test_scaled= scaler.transform(X_test)
        clf = Ridge().fit(X_train_scaled, y_train)
        print("Interseccion (b): {}".format(clf.intercept_))
        print("Pesos (w): {}".format(clf.coef_))
        r2_score = clf.score(X_test_scaled, y_test)
        print("Score - Ridge: {}".format(r2_score))

        print(">>>> Usando Kernel Ridge")






        
