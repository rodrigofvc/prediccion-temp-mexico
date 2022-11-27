import pandas as pd
from datetime import date, timedelta
from datetime import datetime

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

    """
    Toma los registros dentro de un intervalo de tiempo
    """
    def intervalo(self, X, Y, fecha_cercana, fecha_lejana):
        fecha_cercana_dt = datetime.strptime(fecha_cercana, '%Y-%m-%d %H:%M:%S')
        fecha_cercana_fn = datetime.strptime(fecha_lejana, '%Y-%m-%d %H:%M:%S')
        dias_diferencia = fecha_cercana_dt - fecha_cercana_fn
        n = dias_diferencia.days + 1

        X_out = pd.DataFrame(columns=X.columns)
        Y_out = pd.DataFrame(columns=Y.columns)

        index = Y.index[Y['Hora Local'] == fecha_cercana].tolist()
        index = index[0]

        while n != 0:
            row_x = X.iloc[[index]]
            row_y = Y.iloc[[index]]
            X_out = pd.concat([X_out, row_x])
            Y_out = pd.concat([Y_out, row_y])
            index += 1
            n -= 1

        return X_out, Y_out
