import pandas as pd

# Leer el archivo CSV
data = pd.read_csv("san_bernardo.csv")

# Definir la función para procesar el DataFrame
def data_make(df):
    # Eliminar columnas completamente vacías
    df_limpio = df.loc[:, df.notna().sum() > 0]
    
    # Seleccionar columnas específicas
    columnas_necesarias = ["name", "addr.street", "addr.housenumber", "latitude", "longitude"]
    for col in columnas_necesarias:
        if col not in df_limpio.columns:
            raise ValueError(f"La columna '{col}' no existe en el DataFrame.")
    
    # Crear el DataFrame con las columnas seleccionadas
    df_seleccionado = df_limpio[columnas_necesarias]
    return df_seleccionado

# Procesar el DataFrame con la función
try:
    df_procesado = data_make(data)
    print("DataFrame procesado correctamente:")
    print(df_procesado.head())
except Exception as e:
    print("Error al procesar el DataFrame:", e)