#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
from datetime import datetime

from conexionBD import *  #Importando conexion BD
from funciones import *  #Importando mis Funciones
from routes import * #Vistas

import re
from werkzeug.security import generate_password_hash, check_password_hash
## Importacion de loggin para registros
import logging

# Configurar el sistema de logs
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Pagina Principal.
@app.route('/dashboard', methods=['GET', 'POST'])
def loginUser():
    conexion_SQLdb = connectionBD()
    app.logger.info(f'Solicitud GET a {request.path} desde {request.remote_addr}')
  
    if 'conectado' in session:
        perfil_usuario = session['tipo_user']
        #Perfil Desarrollador
        if perfil_usuario in [1,2,3,99,100]:
            return redirect(url_for('inicio'))
    else:
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email      = str(request.form['email'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion_SQLdb.cursor()
            cursor.execute("SELECT * FROM login WHERE email = ?", [email])
            columns = [column[0] for column in cursor.description]
            print (columns)
            account = [dict(zip(columns, row)) for row in cursor.fetchall()][   0]
            if account:
                if check_password_hash(account['password'],password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas 
                    session['conectado']        = True
                    session['id']               = account['id']
                    session['tipo_user']        = account['tipo_user']
                    session['nombre']           = account['nombre']
                    session['apellido']         = account['apellido']
                    session['email']            = account['email']
                    session['perfil_usuario']             = account['perfil_usuario']
                    session['minera']             = account['minera']
                    session['create_at']        = account['create_at']
                    
                    app.logger.info(f'Usuario autenticado: {session}')

                    msg = "Ha iniciado sesión correctamente."
                    return redirect(url_for('loginUser'))  # Redirigir al mismo endpoint para gestionar la redirección basada en el perfil

                else:
                    app.logger.info('Usuario no autenticado')

                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
            else:
                return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
    return render_template('public/modulo_login/index.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0)

#Registrando una cuenta de Usuario
import pyodbc  # Asegúrate de tener el módulo pyodbc instalado

@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    if 'conectado' in session and session['tipo_user'] == 1:
        msg = ''
        conexion_SQLServer = connectionBD()

        if request.method == 'POST':
            if request.form['perfil_usuario'] == 'Ad. Contrato':
                tipo_user = 2
            elif request.form['perfil_usuario'] == 'Cat':
                tipo_user = 100
            elif request.form['perfil_usuario'] == 'Desarrollo  ':
                tipo_user = 1    
            elif request.form['perfil_usuario'] == 'Control Trafico':
                tipo_user = 99
            elif request.form['perfil_usuario'] == 'Sistemas':
                tipo_user = 3
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            password = request.form['password']
            repite_password = request.form['repite_password']
            perfil_usuario = request.form['perfil_usuario']
            minera = request.form['minera']
            create_at = date.today()

            cursor = conexion_SQLServer.cursor()
            cursor.execute('SELECT * FROM login WHERE email = ?', (email,))
            account = cursor.fetchone()

            if account:
                msg = 'Ya existe el Email!'
            elif password != repite_password:
                msg = 'Disculpa, las clave no coinciden!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Disculpa, formato de Email incorrecto!'
            elif not email or not password or not password or not repite_password:
                msg = 'El formulario no debe estar vacío!'
            else:
                password_encriptada = generate_password_hash(password, method='pbkdf2:sha256')
                cursor.execute(
                    'INSERT INTO login(tipo_user, nombre, apellido, email, password, perfil_usuario, minera, create_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (tipo_user, nombre, apellido, email, password_encriptada, perfil_usuario, minera, create_at)
                )
                cursor.commit()
                msg = 'Cuenta creada correctamente!'
            print(msg)
            cursor.close()
            return render_template('public/dashboard/pages/Desarrollo/Administrador_Usuarios.html', msjAlert=msg, typeAlert=1, dataLogin=dataLoginSesion())
        return redirect(url_for('AdministrarUsuarios'))



@app.route('/actualizar-mi-perfil/<id>', methods=['POST'])
def actualizarMiPerfil(id):
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            if(request.form['password']):
                password         = request.form['password'] 
                repite_password  = request.form['repite_password'] 
                print (password, repite_password)
                if (password != repite_password) and (session['tipo_user'] in [1,2,3,99,100]):
                    msg ='Las claves no coinciden'
                    if session['tipo_user'] == 100: 
                        return render_template('public/dashboard/pages/Cat/Profile_CAT.html',msjAlert = msg, typeAlert=0, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                    elif session['tipo_user'] ==2: 
                        return render_template('public/dashboard/pages/Ad. Contrato/Profile_AD.html', msjAlert = msg, typeAlert=0,dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                    elif session['tipo_user'] ==3:
                        print ('----------------', 'No nuestra ms')
                        return render_template('public/dashboard/pages/Sistemas/Profile_Sistemas.html', msjAlert = msg, typeAlert=0, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                    elif session['tipo_user'] ==99:
                        return render_template('public/dashboard/pages/C. Trafico/Profile_CT.html', msjAlert = msg, typeAlert=0,  dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                    elif session['tipo_user'] ==1:
                        return render_template('public/dashboard/pages/Desarrollo/Profile_desarrollo.html', msjAlert = msg, typeAlert=0,  dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                
                
                else:
                    nueva_password = generate_password_hash(password, method='pbkdf2:sha256')
                    actualizar_password_sql_server(nueva_password, id)
                    form = CATForm()
                    msg = 'Perfil actualizado correctamente'
                    print ('----------------CAMBIANDO------------')
                    if session['tipo_user'] == 100: 
                        return render_template('public/dashboard/home_CAT.html',msjAlert = msg, typeAlert=1, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), form = form, data = mostrarRegistros('Pendiente Aprobacion'))
                    elif session['tipo_user'] ==2: 
                        return render_template('public/dashboard/home_Admin.html', msjAlert = msg, typeAlert=1, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))
                    elif session['tipo_user'] ==3:
                        return render_template('public/dashboard/home_Sistemas.html', msjAlert = msg, typeAlert=1, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarRegistros('Aprobado'))
                    elif session['tipo_user'] ==99:
                        return render_template('public/dashboard/home_CT.html', msjAlert = msg, typeAlert=1, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                    elif session['tipo_user'] ==1:
                        return render_template('public/dashboard/home_desarrollo.html', msjAlert = msg, typeAlert=1, dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
                
        else:
            return redirect(url_for('inicio'))
        
    else:
        return redirect(url_for('inicio'))
            

import pyodbc  # Asegúrate de tener el módulo pyodbc instalado

@app.route('/actualizar-perfil', methods=['POST'])
def actualizarPerfil():
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            if request.form['password']:
                password = request.form['password']
                repite_password = request.form['repite_password']

                if (password != repite_password) and (session['tipo_user'] == 1):
                    msg = 'Las claves no coinciden'
                    return render_template('public/dashboard/home_desarrollo.html', msjAlert=msg, typeAlert=0,
                                           dataLogin=dataLoginSesion())
                else:
                    nueva_password = generate_password_hash(password, method='pbkdf2:sha256')
                    conexion_SQLServer = connectionBD()

                    cur = conexion_SQLServer.cursor()
                    cur.execute("""
                        UPDATE login
                        SET                              
                            password = ?
                        WHERE email = ?""", (nueva_password, request.form['correo']))
                    conexion_SQLServer.commit()
                    cur.close()
                    conexion_SQLServer.close()
                    msg = 'Perfil actualizado correctamente'

                    return render_template('public/dashboard/home_desarrollo.html', msjAlert=msg, typeAlert=1,
                                           dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario())

        return render_template('public/dashboard/home_desarrollo.html', msjAlert=msg, typeAlert=1,
                               dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario())





if __name__ == "__main__":
    app.run(debug=True, port=8000)
    
    