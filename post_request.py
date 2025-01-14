import requests
import ast
from api_link import url

def get_info(region,comuna,rol,subrol):
    data = {"region":region,
            "comuna":comuna,
            "rol":rol,
            "subRol":subrol}
    try:
        s = requests.post(url+"/sii/antecedentes",data,timeout=5).content
        dict_str = s.decode("UTF-8")
        return ast.literal_eval(dict_str)
    except requests.Timeout:
        print("La solicitud tomó demasiado tiempo (> 5 segundos).")
        return {}

def get_avaluo(region,comuna,rol,subrol):
    data = get_info(region,comuna,rol,subrol)
    if data == {}:
        return {}
    claves = {'Avalúo Total','Avalúo Exento','Avalúo Afecto','Adicional 0,025% Avalúo Afecto'}
    return {clave:data[clave] for clave in claves if clave in data}

def get_rol(comuna, calle, numero, detalle):
    data = {
        "comuna": comuna,
        "calle": calle,
        "numero": numero,
        "detalle": detalle
    }
    try:
        # Realizar la solicitud con un timeout de 20 segundos
        s = requests.post(url + "/sii/rol", data, timeout=5).content
        dict_str = s.decode("UTF-8")
        dict_str = dict_str.replace("null", '""')
        i = 0
        
        if dict_str != "":
            try:
                dic = ast.literal_eval(dict_str)
                claves = {'manzana', 'predio'}
                return {clave: dic[clave] for clave in claves if clave in dic}
            except Exception as e:
                print(dict_str)
                i += 1
                print(i)
                print(f"except in {i}: {e}")
                return {'manzana': "", 'predio': ""}
        else:
            print("no se encontró el rol")
            return {'manzana': "", 'predio': ""}
    
    except requests.Timeout:
        print("La solicitud tomó demasiado tiempo (> 5 segundos).")
        return {'manzana': "", 'predio': ""}
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return {'manzana': "", 'predio': ""}