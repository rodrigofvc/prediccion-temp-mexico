import pandas as pd
from datetime import date, timedelta
from datetime import datetime
import matplotlib.pyplot as plt

class Lector_Futuro():

    def __init__(self, file):
        self.file = file


    def obtenerUltimaFecha(self, df, horas, diasFuturo = 0):
        for i in range(len(df)):
            ultima_fecha = df.iloc[i-1,0]
            ultima_hora = ultima_fecha.split(" ")[1]
            if(ultima_hora == horas and diasFuturo == 0):
                return datetime.strptime(str(ultima_fecha), '%Y-%m-%d %H:%M:%S')
            elif(ultima_hora == horas):
                diasFuturo -= 1
        return None


    """
    fecha: fecha mas adelante a partir de la cual se van a tomar los registros
        formato: YYYY-MM-DD
    horas: registros a considerar por dia
        formato: HH:MM:SS
    n: numero de registros a considerar por dia
    dias: numero de dias a tomar en cuenta desde la fecha dada hacia atras
    show: indicar si se requiere imprimir las graficas
    """
    def get_data(self, fecha, horas, n, dias, show, pasosFuturo=1, multiSalidas = True):
        df = pd.read_csv(self.file, encoding='utf8', encoding_errors='ignore')
        # Columna basura que se agrega al leer el archivo
        df = df.drop(columns=['Unnamed: 11', 'Fecha UTC'], errors='ignore')

        registros = pd.DataFrame(columns=df.columns)

        excluirColumnas = ["Direcci�n de r�faga (grados)", "Precipitaci�n (mm)"]
        columnasFinal = df.columns[1:].tolist()
        if(multiSalidas):
            tempPasos = 1
            columnasFinal.append("Temperatura prom d_t")
            while(tempPasos <= pasosFuturo):
                    columnasFinal.append("Temperatura d_t+"+str(tempPasos)+"D")
                    tempPasos += 1
        else:
            columnasFinal.extend(["Temperatura prom d_t", "Temperatura d_t+"+str(pasosFuturo)+"D"])
        columnasFinal.remove("Temperatura del Aire (�C)")
        for excolumn in excluirColumnas:
            if excolumn in columnasFinal:
                columnasFinal.remove(excolumn)
        registros = pd.DataFrame(columns=columnasFinal)

        if(fecha is None):
            fecha_actual = self.obtenerUltimaFecha(df, horas, pasosFuturo)
        else:
            fecha_actual = datetime.strptime(fecha + ' ' + horas, '%Y-%m-%d %H:%M:%S')
        fecha_predecir = fecha_actual + timedelta(days=pasosFuturo)
        fecha_actual -= timedelta(minutes=10*(n//2))

        while dias != 0:
            if(multiSalidas):
                    datosPredecirList = []
                    tempPasos = 1
                    print("\n---------------\n")
                    while(tempPasos <= pasosFuturo):
                        print(f"Temperatura de fecha a predecir (Temperatura d_t+{tempPasos}D): {(fecha_predecir - timedelta(days=tempPasos-1))}")
                        datosPredecir = df[df['Fecha Local'].str.contains((fecha_predecir - timedelta(days=tempPasos-1)).strftime('%Y-%m-%d %H:%M:%S'))]
                        datosPredecirList.append(datosPredecir)
                        tempPasos += 1
            else:
                    print(f"\n---------------\nTemperatura de fecha a predecir (Temperatura d_t+{pasosFuturo}D): {fecha_predecir}")
                    datosPredecir = df[df['Fecha Local'].str.contains(fecha_predecir.strftime('%Y-%m-%d %H:%M:%S'))]
            print(f"Datos de 1 día antes, con promedio en ventana de n datos (Temperatura d_t): {fecha_actual}", end=", ")
            temporalDF = pd.DataFrame(columns=df.columns)
            row = df[df['Fecha Local'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
            temporalDF = pd.concat([temporalDF, row])
            i = 0
            while i != n-1:
                    fecha_actual += timedelta(minutes=10)
                    print(f"{fecha_actual}", end=", ")
                    row = df[df['Fecha Local'].str.contains(fecha_actual.strftime('%Y-%m-%d %H:%M:%S'))]
                    temporalDF = pd.concat([temporalDF, row])
                    i += 1
            fecha_actual -= timedelta(minutes=10*(n-1))
            fecha_actual -= timedelta(days=pasosFuturo+1)
            fecha_predecir -= timedelta(days=pasosFuturo+1)
            dias -= 1

            temporalDFMean = temporalDF.drop(columns=["Fecha Local"])
            temporalDFMean = temporalDFMean.drop(columns=excluirColumnas, errors='ignore')
            temporalDFMean = temporalDFMean.mean(axis=0, skipna = True)
            temporalDFMean = pd.DataFrame(temporalDFMean)
            temporalDFMean = temporalDFMean.transpose()
            temporalDFMean["Temperatura prom d_t"] = [float(temporalDFMean["Temperatura del Aire (�C)"])]
            if(multiSalidas):
                    tempPasos = 1
                    while(tempPasos <= pasosFuturo):
                        temporalDFMean["Temperatura d_t+"+str(tempPasos)+"D"] = [float(datosPredecirList[tempPasos-1]["Temperatura del Aire (�C)"])]
                        tempPasos += 1
            else:
                    temporalDFMean["Temperatura d_t+"+str(pasosFuturo)+"D"] = [float(datosPredecir["Temperatura del Aire (�C)"])]
            temporalDFMean = temporalDFMean.drop(columns=["Temperatura del Aire (�C)"])
            registros = pd.concat([registros, temporalDFMean])

        registros = registros.reset_index(drop=True)

        if(multiSalidas == False):
           # Toma la columna 'Temperatura d_t' como Y
            Y = registros[registros.columns[-1:]]
            # Toma los datos de X excluyendo a la temperatura
            X = registros[registros.columns[:-1]]
        else:
            # Toma la columna 'Temperatura d_t' como Y
            Y = registros[registros.columns[-pasosFuturo:]]
            # Toma los datos de X excluyendo a la temperatura
            X = registros[registros.columns[:-pasosFuturo]]

        return X,Y