#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date
from datetime import datetime

from conexionBD import *  #Importando conexion BD
from funciones import *  #Importando mis Funciones
from routes import * #Vistas
from forms import * #Importancion de formularios

import re
from werkzeug.security import generate_password_hash, check_password_hash
import logging ## Importacion de loggin para registros

# Configurar el sistema de logs
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def page_inicio():
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        form = loginUsuario()
        return render_template('public/modulo_login/index.html', form = form)

# Pagina Principal.
@app.route('/dashboard', methods=['GET', 'POST'])
def loginUser():
    app.logger.info(f'Solicitud GET a {request.path} desde {request.remote_addr}')
    print (session)
    if 'conectado' in session:
        perfil_usuario = session['tipo_user']
        #Perfil Desarrollador
        if perfil_usuario in [1,2,3,99,100]:
            return redirect(url_for('inicio'))
    else:
        form = loginUsuario(request.form)
        print (form.validate_on_submit())
        if form.validate_on_submit():
            email      = str(request.form['email'])
            password   = str(request.form['password'])
            
            # Comprobando si existe una cuenta
            account = consultaCuentaExistente(email) 
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
                    flash('Autenticación exitosa!', 'success')

                    return redirect(url_for('loginUser'))  # Redirigir al mismo endpoint para gestionar la redirección basada en el perfil

                else:
                    app.logger.info('Usuario no autenticado')
                    flash('Datos incorrectos, por favor verfique!', 'danger')
                    return redirect(url_for('page_inicio'))
            else:
                return redirect(url_for('page_inicio'))
    return redirect(url_for('page_inicio'))

#Registrando una cuenta de Usuario
import pyodbc  # Asegúrate de tener el módulo pyodbc instalado

@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    if 'conectado' in session and session['tipo_user'] == 1:
        conexion_SQLServer = connectionBD()
        form = crearUsuario(request.form)
        print (form.validate_on_submit())
        print (request.form)
        print (request.form.getlist('minera'))
        if form.validate_on_submit():
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
            minera = str(request.form.getlist('minera'))
            create_at = date.today().strftime('%d-%m-%Y, %H:%M')

            cursor = conexion_SQLServer.cursor()
            cursor.execute('SELECT * FROM login WHERE email = ?', (email,))
            account = cursor.fetchone()

            if account:
                flash ('Ya existe el Email!', 'danger')
            elif password != repite_password:
                flash ('Disculpa, las claves no coinciden!', 'danger')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash ('Disculpa, formato de Email incorrecto!', 'danger')
            else:
                password_encriptada = generate_password_hash(password, method='pbkdf2:sha256')
                cursor.execute(
                    'INSERT INTO login(tipo_user, nombre, apellido, email, password, perfil_usuario, minera, create_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (tipo_user, nombre, apellido, email, password_encriptada, perfil_usuario, minera, create_at)
                )
                cursor.commit()
                flash('Cuenta creada correctamente!', 'success')
                return redirect(url_for('inicio'))

            cursor.close()
            
            return redirect(url_for('AdministrarUsuarios')) 
        return redirect(url_for('AdministrarUsuarios'))

@app.route('/actualizar-mi-perfil', methods=['POST'])
def actualizar_mi_perfil():
    if 'conectado' in session:
        form = cambioPassword(request.form)
        print(form.validate_on_submit())
        if form.validate_on_submit():
            print ('es validado')
            old_password = form.old_password.data
            new_password = form.new_password.data 

            # Verifica si la contraseña actual es correcta
            if verificar_contrasena_actual(session['id'], old_password):
                # Lógica de actualización de contraseñas aquí
                nueva_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                actualizar_password_sql_server(nueva_password, session['id']) 
                # Almacena el mensaje en la sesión flash
                flash('Contraseña cambiada satisfactoriamente', 'success')

                # Redirige a la página de inicio o a donde desees
                return redirect(url_for('inicio'))
            else:
                flash("La contraseña actual no es correcta", 'danger')
                return redirect(url_for('inicio'))

        else:
            # Almacena los errores de validación en la sesión flash
            flash(f"La nueva contraseña no coincide", 'danger')

            # Redirige de nuevo al formulario con los mensajes flash
            return redirect(url_for('inicio'))
    else:
        return redirect(url_for('inicio'))

@app.route('/actualizar-perfil', methods=['POST'])
def actualizarPerfil():
    if 'conectado' in session:
        msg = ''
        form = ediotarUsuario(request.form)
        print (form.validate_on_submit())
        if form.validate_on_submit():
            conexion_SQLServer = connectionBD()
            cursor = conexion_SQLServer.cursor()
            cursor.execute('SELECT * FROM login WHERE email = ?', (request.form['email'],))
            account = cursor.fetchone()

            password = request.form['password']
            repite_password = request.form['repite_password']

            if account:
                if (password != repite_password) and (session['tipo_user'] == 1):
                    msg = 'Las claves no coinciden'
                    flash(msg, 'danger')
                    return redirect(url_for('editProfileUsers'))
                else:
                    nueva_password = generate_password_hash(password, method='pbkdf2:sha256')
                    conexion_SQLServer = connectionBD()

                    cur = conexion_SQLServer.cursor()
                    cur.execute("""
                        UPDATE login
                        SET                              
                            password = ?
                        WHERE email = ?""", (nueva_password, request.form['email']))
                    conexion_SQLServer.commit()
                    cur.close()
                    conexion_SQLServer.close()
                    msg = 'Perfil actualizado correctamente'
                    flash (msg, 'success')

                    return render_template('public/dashboard/home_desarrollo.html', dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario())
            else: 
                flash('La cuenta no existe', 'danger')
                return redirect(url_for('editProfileUsers'))
 

        return render_template('public/dashboard/home_desarrollo.html', msjAlert=msg, typeAlert=1,
                               dataLogin=dataLoginSesion(), dataUser=dataPerfilUsuario())


if __name__ == "__main__":
    app.run(debug=True, port=8000)
    
    