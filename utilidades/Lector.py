import pandas as pd
from datetime import date, timedelta

class Lector():

    def __init__(self, file):
        self.file = file


    """
    fecha: fecha mas adelante a partir de la cual se van a tomar los registros
        formato: YYYY-MM-DD
    horas: registros a considerar por dia
        formato: HH:MM:SS
    dias: numero de dias a tomar en cuenta desde la fecha dada hacia atras
    """
    def get_data(self, fecha, horas, dias):
        df = pd.read_csv(self.file, encoding='utf8', encoding_errors='ignore')
        # Columna basura que se agrega al leer el archivo
        df = df.drop(columns=['Unnamed: 11'])

        registros = pd.DataFrame(columns=df.columns)

        fecha_actual = date.fromisoformat(fecha)

        while dias != 0:
            for hora in horas:
                row = df[df['Fecha UTC'].str.contains(fecha_actual.isoformat() + ' ' + hora)]
                registros = pd.concat([registros, row])
            fecha_actual -= timedelta(days=1)
            dias -= 1
        print(registros)

        # Toma la columna 'Temperatura del Aire (°C)' como Y
        columna_temperatura = registros.columns[6]
        Y = registros.get([columna_temperatura])
        print(Y)
        # Elimina las columnas con datos no numericos
        registros = registros.drop(columns=['Fecha Local', 'Fecha UTC'])
        # Toma los datos de X excluyendo a la temperatura
        X = registros.drop(columna_temperatura, axis=1)
        print(X)
        return X,Y
