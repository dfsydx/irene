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
    dict_str = dict_str.replace("null",'\"\"')
    i = 0
    if dict_str != "":
        try:
            dic = ast.literal_eval(dict_str)
            claves = {'manzana','predio'}
            return {clave:dic[clave] for clave in claves if clave in dic}
        except:
            print(dict_str)
            i = i+1
            print(i)
            return {'manzana':"",'predio':""}
    else:
        print("ok")
        return {'manzana':"",'predio':""}

print(get_rol("SAN BERNARDO","Eyzaguirre","1094",""))

# latitud, longitud, avaluo, número de la calle