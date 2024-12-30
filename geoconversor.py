import geopandas as gpd
import pandas as pd

def geojson_to_csv(geojson_file, csv_file):
    # Leer el archivo GeoJSON
    geojson_data = gpd.read_file(geojson_file)
    
    # Crear listas vacías para las coordenadas
    latitudes = []
    longitudes = []
    
    # Iterar sobre las geometrías
    for geometry in geojson_data.geometry:
        if geometry.geom_type == 'Point':
            latitudes.append(geometry.y)
            longitudes.append(geometry.x)
        elif geometry.geom_type == 'Polygon' or geometry.geom_type == 'MultiPolygon':
            # Extraer el centroide de un Polígono o Multipólígono
            latitudes.append(geometry.centroid.y)
            longitudes.append(geometry.centroid.x)
        elif geometry.geom_type == 'LineString' or geometry.geom_type == 'MultiLineString':
            # Para LineString y MultiLineString, tomar el primer punto
            latitudes.append(geometry.coords[0][1])
            longitudes.append(geometry.coords[0][0])
        else:
            # Para otros tipos de geometrías, agregar NaN o algún valor
            latitudes.append(None)
            longitudes.append(None)
    
    # Agregar las coordenadas al GeoDataFrame
    geojson_data['latitude'] = latitudes
    geojson_data['longitude'] = longitudes
    
    # Convertir a un DataFrame de pandas (sin la columna de geometría)
    df = geojson_data.drop(columns='geometry')
    
    # Guardar como CSV
    df.to_csv(csv_file, index=False)

# Usar la función
#geojson_to_csv("/home/pipe/irene/san_bernardo.geojson", "/home/pipe/irene/san_bernardo.csv")

# Leer el archivo CSV
data = pd.read_csv("san_bernardo.csv")

# Mostrar nombres de las columnas para depurar
print("Columnas disponibles en el DataFrame:", data.columns)

# Definir la función para procesar el DataFrame
def data_make(df):
    # Eliminar columnas vacías
    df_limpio = df.loc[:, df.notna().sum() > 0]
    
    # Asegurarse de que los nombres de las columnas no tengan espacios adicionales
    df_limpio.columns = df_limpio.columns.str.strip()
    
    # Filtrar filas donde 'addr.country' sea "CL"
    if "addr.country" in df_limpio.columns:
        df_filtrado = df_limpio[df_limpio["addr.country"] == "CL"]
    else:
        raise ValueError("La columna 'addr.country' no se encuentra en el DataFrame después de limpiar.")
    
    # Seleccionar columnas específicas
    columnas_necesarias = ["name", "addr.street", "addr.housenumber", "latitude", "longitude"]
    columnas_presentes = [col for col in columnas_necesarias if col in df_filtrado.columns]
    
    if len(columnas_presentes) < len(columnas_necesarias):
        print("Advertencia: Algunas columnas necesarias no están presentes en el DataFrame.")
    
    df_seleccionado = df_filtrado[columnas_presentes]
    return df_seleccionado

# Procesar el DataFrame
try:
    df_procesado = data_make(data)
    print(df_procesado)
except Exception as e:
    print(f"Ocurrió un error: {e}")