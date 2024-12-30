import requests
import ast
from api_link import url

def get_info(region,comuna,rol,subrol):
    data = {"region":region,
            "comuna":comuna,
            "rol":rol,
            "subRol":subrol}
    s = requests.post(url+"/sii/antecedentes",data).content
    dict_str = s.decode("UTF-8")
    return ast.literal_eval(dict_str)

def get_avaluo(region,comuna,rol,subrol):
    data = get_info(region,comuna,rol,subrol)
    claves = {'Avalúo Total','Avalúo Exento','Avalúo Afecto','Adicional 0,025% Avalúo Afecto'}
    return {clave:data[clave] for clave in claves if clave in data}

def get_rol(comuna,calle,numero,detalle):
    data = {"comuna":comuna,
            "calle":calle,
            "numero":numero,
            "detalle":detalle}
    s = requests.post(url+"/sii/rol",data).content
    dict_str = s.decode("UTF-8")
    if dict_str != "":
        dic = ast.literal_eval(dict_str)
        claves = {'manzana','predio'}
        return {clave:dic[clave] for clave in claves if clave in dic}
    else: 
        return {'manzana':"",'predio':""}

# latitud, longitud, avaluo, número de la calle