#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
from datetime import datetime

from conexionBD import *  #Importando conexion BD
from funciones import *  #Importando mis Funciones
from routes import * #Vistas

import re
from werkzeug.security import generate_password_hash, check_password_hash


# Pagina Principal.
@app.route('/dashboard', methods=['GET', 'POST'])
def loginUser():
    conexion_MySQLdb = connectionBD()
    print (session)
    if 'conectado' in session:
        perfil_usuario = session['tipo_user']
        print (perfil_usuario)
        #Perfil Desarrollador
        if perfil_usuario == 1:
            return render_template('public/dashboard/home_desarrollo.html', dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario(), data=mostrarRegistros('Pendiente Aprobacion'))
        #Perfil Cat
        elif perfil_usuario == 100:
            form = CATForm()
            return render_template('public/dashboard/home_CAT.html', dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario(), data=mostrarRegistros('Pendiente Aprobacion'), form = form)
        #Perfil Ad. Contrato
        elif perfil_usuario == 2:
            return render_template('public/dashboard/home_Admin.html', dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))
        #Perfil Sistemas
        elif perfil_usuario == 3:
            return render_template('public/dashboard/home_Sistemas.html', dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario(), data = mostrarRegistros('Aprobado'))
        elif perfil_usuario == 99:
            return redirect(url_for('historial'))

    else:
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email      = str(request.form['email'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM login_python WHERE email = %s", [email])
            account = cursor.fetchone()

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
                    session['agencia_financiera']     = account['agencia_financiera']
                    
                    msg = "Ha iniciado sesión correctamente."
                    return redirect(url_for('loginUser'))  # Redirigir al mismo endpoint para gestionar la redirección basada en el perfil

                else:
                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
            else:
                return render_template('public/modulo_login/index.html', msjAlert = msg, typeAlert=0)
    return render_template('public/modulo_login/index.html', msjAlert = 'Debe iniciar sesión.', typeAlert=0)

#Registrando una cuenta de Usuario
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    if ('conectado' in session) and (session['tipo_user'] ==1):
        msg = ''
        conexion_MySQLdb = connectionBD()
        if request.method == 'POST':
            if request.form['perfil_usuario'] == 'Ad. Contrato':
                tipo_user = 2
            elif request.form['perfil_usuario'] == 'Cat':
                tipo_user = 100
            elif request.form['perfil_usuario'] == 'Control Trafico':
                tipo_user = 99
            elif request.form['perfil_usuario'] == 'Sistemas':
                tipo_user = 3
            nombre                      = request.form['nombre']
            apellido                    = request.form['apellido']
            email                       = request.form['email']
            password                    = request.form['password']
            repite_password             = request.form['repite_password']
            perfil_usuario                        = request.form['perfil_usuario']
            minera                        = request.form['minera']
            create_at                   = date.today()
            #current_time = datetime.datetime.now()

            # Comprobando si ya existe la cuenta de Usuario con respecto al email
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute('SELECT * FROM login_python WHERE email = %s', (email,))
            account = cursor.fetchone()
            cursor.close() #cerrrando conexion SQL
            
            if account:
                msg = 'Ya existe el Email!'
            elif password != repite_password:
                msg = 'Disculpa, las clave no coinciden!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Disculpa, formato de Email incorrecto!'
            elif not email or not password or not password or not repite_password:
                msg = 'El formulario no debe estar vacio!'
            else:
                # La cuenta no existe y los datos del formulario son válidos,
                password_encriptada = generate_password_hash(password, method='pbkdf2:sha256')
                conexion_MySQLdb = connectionBD()
                cursor = conexion_MySQLdb.cursor(dictionary=True)
                cursor.execute('INSERT INTO login_python (tipo_user, nombre, apellido, email, password, perfil_usuario, minera, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (tipo_user, nombre, apellido, email, password_encriptada, perfil_usuario, minera, create_at))
                conexion_MySQLdb.commit()
                cursor.close()
                msg = 'Cuenta creada correctamente!'
            print (msg)
            return render_template('public/dashboard/pages/Desarrollo/Administrador_Usuarios.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion())
        return redirect(url_for('AdministrarUsuarios'))


@app.route('/actualizar-mi-perfil/<id>', methods=['POST'])
def actualizarMiPerfil(id):
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            if(request.form['password']):
                password         = request.form['password'] 
                repite_password  = request.form['repite_password'] 
                
                if (password != repite_password) and (session['tipo_user'] == 100):
                    msg ='Las claves no coinciden'
                    return render_template('public/dashboard/home_CAT.html', msjAlert = msg, typeAlert=0, dataLogin = dataLoginSesion(), data=mostrarRegistros('Pendiente Aprobacion'))
                elif (password != repite_password) and (session['tipo_user'] == 2):
                    msg ='Las claves no coinciden'
                    return render_template('public/dashboard/home_Admin.html', msjAlert = msg, typeAlert=0, dataLogin = dataLoginSesion(),data = mostrarRegistros('Pendiente Aprobacion', session['minera']))
                elif (password != repite_password) and (session['tipo_user'] == 3):
                    msg ='Las claves no coinciden'
                    return render_template('public/dashboard/home_Sistemas.html',  msjAlert = msg, typeAlert=0, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Aprobado'))

                else:
                    nueva_password = generate_password_hash(password, method='pbkdf2:sha256')
                    conexion_MySQLdb = connectionBD()
                    cur = conexion_MySQLdb.cursor()
                    cur.execute("""
                        UPDATE login_python 
                        SET                              
                            password = %s
                        WHERE id = %s""", (nueva_password, id))
                    conexion_MySQLdb.commit()
                    cur.close() #Cerrando conexion SQL
                    conexion_MySQLdb.close() #cerrando conexion de la BD
                    msg = 'Perfil actualizado correctamente'
                    if session['tipo_user'] == 100:
                        return render_template('public/dashboard/home_CAT.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), data=mostrarRegistros('Pendiente Aprobacion'))
                    elif session['tipo_user'] == 2:
                        return render_template('public/dashboard/home_Admin.html', msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))
                    elif session['tipo_user'] == 3:
                        return render_template('public/dashboard/home_Sistemas.html',  msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Aprobado'))
                    elif session['tipo_user'] == 1:
                        return render_template('public/dashboard/home_Admin.html',  msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario())


            
        if session['tipo_user'] == 100:
            return render_template('public/dashboard/home_CAT.html', dataLogin = dataLoginSesion(), data=mostrarRegistros('Pendiente Aprobacion'))             
        elif session['tipo_user'] == 2:
            return render_template('public/dashboard/home_Admin.html', dataLogin = dataLoginSesion(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))   
        elif session['tipo_user'] == 3: 
            return render_template('public/dashboard/home_Sistemas.html', dataLogin=dataLoginSesion(), data = mostrarRegistros('Aprobado'))
        elif session['tipo_user'] == 1:
            return render_template('public/dashboard/home_Admin.html',  msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario())



@app.route('/actualizar-perfil', methods=['POST'])
def actualizarPerfil():
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            if(request.form['password']):
                password         = request.form['password'] 
                repite_password  = request.form['repite_password'] 
                
                if (password != repite_password) and (session['tipo_user'] == 1):
                    msg ='Las claves no coinciden'
                    return render_template('public/dashboard/home_Admin.html', msjAlert = msg, typeAlert=0, dataLogin = dataLoginSesion(), data=mostrarRegistros('Pendiente Aprobacion'))
                
                else:
                    nueva_password = generate_password_hash(password, method='pbkdf2:sha256')
                    conexion_MySQLdb = connectionBD()
                    cur = conexion_MySQLdb.cursor()
                    cur.execute("""
                        UPDATE login_python 
                        SET                              
                            password = %s
                        WHERE email = %s""", (nueva_password, request.form['correo']))
                    conexion_MySQLdb.commit()
                    cur.close() #Cerrando conexion SQL
                    conexion_MySQLdb.close() #cerrando conexion de la BD
                    msg = 'Perfil actualizado correctamente'   
                    
                    return render_template('public/dashboard/home_Admin.html',  msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario())
                                
        
        return render_template('public/dashboard/home_Admin.html',  msjAlert = msg, typeAlert=1, dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario())




if __name__ == "__main__":
    app.run(debug=True, port=8000)
    
    