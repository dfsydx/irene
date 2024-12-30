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
geojson_to_csv("/home/pipe/Documents/irene/san_bernardo.geojson", "/home/pipe/Documents/irene/san_bernardo.csv")