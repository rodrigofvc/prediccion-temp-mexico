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
    horas: horario a considerar
        formato: HH:MM:SS
    pasosPasado: numero de dias a tomar en cuenta hacia atras
    pasosFuturo: número de pasos a tomaren cuenta hacía el futuro
    excluirColumnasX: lista de columnas a excluir de la variable df (dataframe de datos)
	agregarHoraLocalY: agrega la hora local a la temperatura a predecir (Y)
    show: indicar si se requiere imprimir
    """
    def get_data(self, horas, pasosPasado=1, pasosFuturo=1, excluirColumnasX=["Direcci�n del Viento (grados)","Direcci�n de r�faga (grados)"], agregarHoraLocalY = False, show=True):
        if(pasosFuturo < 1):
          print("[Error]: La variable pasosFuturo debe ser 1 o mayor.")
          return None,None
        if(pasosPasado < 1):
          print("[Error]: La variable pasosPasado debe ser 1 o mayor.")
          return None,None
        df = pd.read_csv(self.file, encoding='utf8', encoding_errors='ignore')

        # Columna basura que se agrega al leer el archivo
        df = df.drop(columns=['Unnamed: 11', 'Fecha UTC'], errors='ignore')
        # Se calcula la fecha más reciente en el horario especificado, dejando pasosFuturo adelante de esta fecha
        fecha_mas_reciente_valida = self.obtenerUltimaFecha(df, horas, pasosFuturo)
        # Se eliminan todas las filas que no sean de la hora especificada
        df = df[df['Fecha Local'].str.contains(horas)]
        df2 = df.copy()
        # Remueve otras columnas pasadas por parámetros de la función
        df = df.drop(columns=excluirColumnasX, errors='ignore')

        # Crea la lista con el nombre de las columnas de la matriz X
        columnasX = []
        # Crea las columnas de la matriz X dependiendo de los pasos pasados
        for i in range(pasosPasado):
          columnasPasoPasado = df.columns[1:].tolist()
          for j in range(len(columnasPasoPasado)):
            columnasPasoPasado[j] += " t-" + str(i+1) + "D"
          columnasX += columnasPasoPasado

        if(agregarHoraLocalY):
          columnasY = ["Temperatura del Aire (�C) t", "Hora Local"]
        else:
          columnasY = ["Temperatura del Aire (�C) t"]

        # Se crea la matriz X con las columnas definidas anteriormente
        X = pd.DataFrame(columns=columnasX)
        Y = pd.DataFrame(columns=columnasY)

        # Se obtiene la primer fecha a predecir con pasos en el futuro
        fecha_predecir = fecha_mas_reciente_valida + timedelta(days = pasosFuturo)

        ready = False
        while not ready: #Cuando ya no sea posible obtener una fecha futura
          datosPredecir = df2[df2['Fecha Local'].str.contains(fecha_predecir.strftime('%Y-%m-%d %H:%M:%S'))]
          if(datosPredecir.shape[0] == 0):
            ready = True
          else:
            temperaturaPredecir = float(datosPredecir["Temperatura del Aire (�C)"])
            if(show):
              print(f"\n---------------\nTemperatura de fecha a predecir (Temperatura d_t = {temperaturaPredecir}): {fecha_predecir}")

          rowFinal = []
          for i in range(pasosPasado):
            row = df[df['Fecha Local'].str.contains(fecha_mas_reciente_valida.strftime('%Y-%m-%d %H:%M:%S'))]
            if(row.shape[0] != 0):
              rowList = row.squeeze().tolist()[1:]
              rowFinal += rowList
              if(show):
                print(f"Datos de t-{i+pasosFuturo} días antes: {fecha_mas_reciente_valida} {rowList}", end="\n")
            else:
              if(show):
                print(f"Ya no hay más datos hacía atras, o la fecha {fecha_mas_reciente_valida} no existe, se omite esta última instancia y termina la iteracion.")
            fecha_mas_reciente_valida -= timedelta(days=1)
          if(len(rowFinal) == 0 or len(rowFinal) < X.shape[1]):
            ready = True
          if(ready == False):
            if(show):
              print(f"Datos pasados final: {rowFinal}", end="\n---------------")
            row_Xdf = pd.DataFrame([rowFinal], columns=columnasX)
            if(agregarHoraLocalY):
              temperatura_Ydf = pd.DataFrame([[temperaturaPredecir, fecha_predecir]], columns=columnasY)
            else:
              temperatura_Ydf = pd.DataFrame([[temperaturaPredecir]], columns=columnasY)
            X = pd.concat([X, row_Xdf])
            Y = pd.concat([Y, temperatura_Ydf])
            fecha_mas_reciente_valida += timedelta(days=pasosPasado-1)
            fecha_predecir -= timedelta(days=1)

        X = X.reset_index(drop=True)
        Y = Y.reset_index(drop=True)

        return X,Y