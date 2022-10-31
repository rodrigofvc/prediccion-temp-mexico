import pandas as pd

class Lector():

    def __init__(self, file):
        self.file = file


    def get_data(self):
        df = pd.read_csv(self.file, encoding='utf8', encoding_errors='ignore')
        # Columna basura que se agrega al leer el archivo
        df = df.drop(columns=['Unnamed: 11'])
        # Filtra todas las mediciones de las 00:00
        df = df[df['Fecha UTC'].str.contains('00:00:00')]
        print(df)
        # Toma la columna 'Temperatura del Aire (°C)' como Y
        y = df.columns[6]
        Y = df.get([y])
        print(Y)
        # Elimina las columnas con datos no numericos
        df = df.drop(columns=['Fecha Local','Fecha UTC'])
        # Toma los datos de X excluyendo a la temperatura
        X = df.drop(df.columns[4],axis=1)
        print(X)
        return X,Y
