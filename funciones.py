import os
from random import sample
from werkzeug.utils import secure_filename 
from flask import session
from conexionBD import * 

#https://pynative.com/python-mysql-database-connection/
#https://pynative.com/python-mysql-select-query-to-fetch-data/


#creando una funcion y dentro de la misma una data (un diccionario)
#con valores del usuario ya logueado
def dataLoginSesion():
    inforLogin = {
        "idLogin"             :session['id'],
        "tipoLogin"           :session['tipo_user'],
        "nombre"              :session['nombre'],
        "apellido"            :session['apellido'],
        "emailLogin"          :session['email'],
        "perfil_usuario"                :session['perfil_usuario'],
        "minera"                      :session['minera'],
        "create_at"                 :session['create_at']
        }
    return inforLogin

def dataPerfilUsuario():
    conexion_SQLdb = connectionBD()
    
    if conexion_SQLdb:
        try:
            cursor = conexion_SQLdb.cursor()
            idUser = session['id']            
            querySQL = "SELECT * FROM login_python WHERE id = ?"            
            cursor.execute(querySQL, [idUser])            
            columns = [column[0] for column in cursor.description]            
            datosUsuario = [dict(zip(columns, row)) for row in cursor.fetchall()][0]             
            return datosUsuario
        except Exception as e:
            print(f"Error al obtener datos de usuario: {str(e)}")
            return None
        finally:
            cursor.close()  # Cerrando el cursor
            conexion_SQLdb.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")
        return None



def stringAleatorio():
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio

def recibeZip(file):
    print(file)
    basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
    filename = secure_filename(file.filename) #Nombre original del archivo

    #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
    extension           = os.path.splitext(filename)[1]
    nuevoNombreFile     = stringAleatorio() + extension
    #print(nuevoNombreFile)
        
    upload_path = os.path.join (basepath, 'static/assets/uploads', nuevoNombreFile) 
    file.save(upload_path)

    return nuevoNombreFile

