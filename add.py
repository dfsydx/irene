from post_request import *
import pandas as pd

def addrol(comuna, csv):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(csv)

    # Crear la nueva columna 'rol'
    rol_column = []
    
    # Iterar sobre las filas del DataFrame y aplicar get_rol
    for _, row in df.iterrows():  # Usamos el _ en lugar de index
        rol_value = get_rol(comuna, row['addr:street'], row['addr:housenumber'], "")
        rol_column.append(rol_value["manzana"]+rol_value["predio"])

    # Asignar la columna 'rol' al DataFrame
    df['rol'] = rol_column

    # Devolver el DataFrame con la nueva columna
    return df

addrol("SAN BERNARDO","san_bernardo_limpio.csv")
