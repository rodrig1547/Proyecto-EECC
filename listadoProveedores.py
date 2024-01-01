from Consultas_sql import maestro
import pandas as pd

def get_minera():

    lista = [('','-----')]
    df = pd.DataFrame(maestro('minera'))
    for item in df['minera'].to_list():
        lista.append((item,item))

    return lista

def get_proveedores():
    lista = [('','-----')]
    df = pd.DataFrame(maestro('empresa'))
    for item in df['empresa'].to_list():
        lista.append((item,item))

    return lista
