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
        "create_at"                 :session['create_at'],
        "agencia_financiera"  :session['agencia_financiera']
    }
    return inforLogin

def dataPerfilUsuario():
    conexion_MySQLdb = connectionBD() 
    mycursor       = conexion_MySQLdb.cursor(dictionary=True)
    idUser         = session['id']
    
    querySQL  = ("SELECT * FROM login_python WHERE id='%s'" % (idUser,))
    mycursor.execute(querySQL)
    datosUsuario = mycursor.fetchone() 
    mycursor.close() #cerrrando conexion SQL
    conexion_MySQLdb.close() #cerrando conexion de la BD
    return datosUsuario



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

