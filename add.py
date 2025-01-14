from post_request import *
import pandas as pd
from data_maker import *

def addrol(comuna, csv):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(csv)
    N = df.shape[0]

    # Crear la nueva columna 'rol'
    rol_column = []
    avaluo_column = []
    
    # Iterar sobre las filas del DataFrame y aplicar get_rol
    for index, row in df.iterrows():  # Usamos el _ en lugar de index
        rol_value = get_rol(comuna, row['addr:street'], row['addr:housenumber'], "")
        rol_column.append(str(rol_value["manzana"])+"-"+str(rol_value["predio"]))
        t = str(rol_value["manzana"])+"-"+str(rol_value["predio"])
        aval_dict = get_avaluo("METROPOLITANA",comuna,rol_value["manzana"],rol_value["predio"])

        if t != '-' and 'Avalúo Total' in aval_dict:
            avaluo_value = aval_dict['Avalúo Total']
            print(avaluo_value)
            if avaluo_value != "":
                avaluo_column.append(str(avaluo_value))
        else:
            avaluo_column.append("")
        print(str(index+1)+"/"+str(N))

    # Asignar la columna 'rol' al DataFrame
    df['rol'] = rol_column
    df['avaluo'] = avaluo_column

    # Devolver el DataFrame con la nueva columna
    return df.to_csv("addrol_"+csv, index=False)

data = addrol("SAN BERNARDO","san_bernardo_limpio.csv")