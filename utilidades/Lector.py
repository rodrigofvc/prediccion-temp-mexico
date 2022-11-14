import pandas as pd
from datetime import date, timedelta
from datetime import datetime
import matplotlib.pyplot as plt

class Lector():

    def __init__(self, file):
        self.file = file


    """
    fecha: fecha mas adelante a partir de la cual se van a tomar los registros
        formato: YYYY-MM-DD
    horas: registros a considerar por dia
        formato: HH:MM:SS
    n: numero de registros a considerar por dia
    dias: numero de dias a tomar en cuenta desde la fecha dada hacia atras
    show: indicar si se requiere imprimir las graficas
    """
    def get_data(self, fecha, horas, n, dias, show, dias_futuro):
        df = pd.read_csv(self.file, encoding='utf8', encoding_errors='ignore')
        # Columna basura que se agrega al leer el archivo
        df = df.drop(columns=['Unnamed: 11'])

        registros = pd.DataFrame(columns=df.columns)

        fecha_actual = datetime.strptime(fecha + ' ' + horas, '%Y-%m-%d %H:%M:%S')
        # Toma desde unos registros antes al punto requerido
        fecha_actual -= timedelta(minutes=10*(n//2))

        while dias != 0:
            row = df[df['Fecha UTC'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
            registros = pd.concat([registros, row])
            i = 0
            while i != n:
                fecha_actual += timedelta(minutes=10)
                row = df[df['Fecha UTC'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
                registros = pd.concat([registros, row])
                i += 1
            fecha_actual -= timedelta(minutes=10*n)
            fecha_actual -= timedelta(days=1)
            dias -= 1

        #Obten tambien registros de algunos dias a futuro
        fecha_actual = datetime.strptime(fecha + ' ' + horas, '%Y-%m-%d %H:%M:%S')
        fecha_actual -= timedelta(minutes=10*(n//2))
        fecha_actual += timedelta(days=1)
        i = 0
        Z = pd.DataFrame(columns=df.columns)
        while i != dias_futuro:
            row = df[df['Fecha UTC'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
            Z = pd.concat([Z, row])
            j = 0
            while j != n:
                fecha_actual += timedelta(minutes=10)
                row = df[df['Fecha UTC'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
                Z = pd.concat([Z, row])
                j += 1
            fecha_actual -= timedelta(minutes=10*n)
            fecha_actual += timedelta(days=1)
            i += 1
        X_unknow = Z

        print(registros)

        # Toma la columna 'Temperatura del Aire (°C)' como Y
        columna_temperatura = registros.columns[6]
        Y = registros.get([columna_temperatura])
        print("\n--------> Y \n")
        print(Y)

        Z1 = Z.get([columna_temperatura])

        # Elimina las columnas con datos no numericos
        registros = registros.drop(columns=['Fecha Local', 'Fecha UTC'])
        # Toma los datos de X excluyendo a la temperatura
        X = registros.drop(columna_temperatura, axis=1)
        # Elimina los registros de direccion de viento y rafaga
        direccion_viento = registros.columns[0]
        direccion_rafaga = registros.columns[1]
        X = X.drop(direccion_viento, axis=1)
        X = X.drop(direccion_rafaga, axis=1)
        
        X_unknow = X_unknow.drop(columns=['Fecha Local', 'Fecha UTC'])
        X_unknow = X_unknow.drop(columna_temperatura, axis=1)
        print("\n--------> X \n")
        print(X)

        fig, axs = plt.subplots(2, 4)

        # Direccion del viento
        axs[0,0].plot(registros.get([registros.columns[0]]), '-o', label=registros.columns[0])
        axs[0,0].legend(loc="upper left")
        axs[0,0].set_title(registros.columns[0])

        # Direccion de rafaga
        axs[0,1].plot(registros.get([registros.columns[1]]), '-o', label=registros.columns[1])
        axs[0,1].legend(loc="upper left")
        axs[0,1].set_title(registros.columns[1])

        # Rapidez del viento
        axs[0,2].plot(registros.get([registros.columns[2]]), '-o', label=registros.columns[2])
        axs[0,2].legend(loc="upper left")
        axs[0,2].set_title(registros.columns[2])

        # Rapidez de rafaga
        axs[0,3].plot(registros.get([registros.columns[3]]), '-o', label=registros.columns[3])
        axs[0,3].legend(loc="upper left")
        axs[0,3].set_title(registros.columns[3])

        # Humedad relativa
        axs[1,0].plot(registros.get([registros.columns[5]]), '-o', label=registros.columns[5])
        axs[1,0].legend(loc="upper left")
        axs[1,0].set_title(registros.columns[5])

        # Presion atmosferica
        axs[1,1].plot(registros.get([registros.columns[6]]), '-o', label=registros.columns[6])
        axs[1,1].legend(loc="upper left")
        axs[1,1].set_title(registros.columns[6])

        # Precipitacion
        axs[1,2].plot(registros.get([registros.columns[7]]), '-o', label=registros.columns[7])
        axs[1,2].legend(loc="upper left")
        axs[1,2].set_title(registros.columns[7])

        # Radiacion
        axs[1,3].plot(registros.get([registros.columns[8]]), '-o', label=registros.columns[8])
        axs[1,3].legend(loc="upper left")
        axs[1,3].set_title(registros.columns[8])

        if show:
            plt.show()

        return X,Y,Z1,X_unknow
