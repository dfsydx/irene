from post_request import *
import pandas as pd
from data_maker import *

def addrol(comuna, csv):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(csv)
    N = df.shape[0]

    # Crear columnas vacías para 'rol' y 'avaluo' si no existen
    if 'rol' not in df.columns:
        df['rol'] = ""
    if 'avaluo' not in df.columns:
        df['avaluo'] = ""

    # Iterar sobre las filas del DataFrame y aplicar get_rol
    for index, row in df.iterrows():
        # Verificar si ya existe un valor en 'rol' para evitar reprocesar
        if df.at[index, 'rol'] == "":
            rol_value = get_rol(comuna, row['addr:street'], row['addr:housenumber'], "")
            rol_string = str(rol_value["manzana"]) + "-" + str(rol_value["predio"])
            df.at[index, 'rol'] = rol_string

            aval_dict = get_avaluo("METROPOLITANA", comuna, rol_value["manzana"], rol_value["predio"])

            if rol_string != '-' and 'Avalúo Total' in aval_dict:
                avaluo_value = aval_dict['Avalúo Total']
                if avaluo_value != "":
                    df.at[index, 'avaluo'] = str(avaluo_value)

        # Guardar el DataFrame actualizado tras procesar cada fila
        partial_csv_name = f"addrol_partial_{index + 1}.csv"
        df.iloc[:index + 1].to_csv(partial_csv_name, index=False)

        # Mostrar progreso
        print(f"{index + 1}/{N} filas procesadas. Guardado en {partial_csv_name}")

    # Guardar el archivo final completo
    final_csv_name = "addrol_" + csv
    df.to_csv(final_csv_name, index=False)
    print(f"Proceso completo. Archivo final guardado en {final_csv_name}")

    # Devolver el nombre del archivo CSV final
    return final_csv_name