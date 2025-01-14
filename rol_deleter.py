import pandas as pd

# Leer el archivo CSV
data = pd.read_csv("san_bernardo.csv")

# Eliminar filas donde la columna 'rol' tenga un '-'
data_filtrado = data[data["rol"] != "-"]

# Guardar el DataFrame filtrado como un nuevo archivo CSV
data_filtrado.to_csv("san_bernardo_data.csv", index=False)

print("Filtrado completado")