from flask import Flask, render_template, redirect, url_for, session, request, send_from_directory, flash, jsonify, send_file
from funciones import *  #Importando mis Funciones
from Consultas_sql import *
from datetime import datetime
from forms import CATForm, historialForm, cambioPassword,loginUsuario, crearUsuario, ediotarUsuario
import pytz #Libraria zona horaria
import ast #transformar str to list
import pandas as pd
import io



#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'

#Zona Horaria Chile
chile_tz = pytz.timezone('Chile/Continental')


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        form = loginUsuario()
        return render_template('public/modulo_login/index.html', form = form)
    
#Decorador de inicio de session
@app.route('/home')
def inicio():
    if 'conectado' in session: 
        perfil_usuario = session['tipo_user']
        if perfil_usuario == 100:
            form = CATForm()
            id_user = session['id']
            return render_template('public/dashboard/home_CAT.html', dataLogin = dataLoginSesion(), data = mostrarRegistros(perfil_usuario= perfil_usuario, id_user = id_user), form = form)
        elif perfil_usuario == 1:
            return (render_template('public/dashboard/home_desarrollo.html', dataLogin = dataLoginSesion()))
        elif perfil_usuario == 2:
            return render_template('public/dashboard/home_Admin.html', dataLogin = dataLoginSesion(), data = mostrarRegistros(perfil_usuario= perfil_usuario, cliente = ast.literal_eval(session['minera'])))
        elif perfil_usuario == 3:
            return render_template('public/dashboard/home_Sistemas.html', dataLogin = dataLoginSesion(), data = mostrarRegistros(perfil_usuario=perfil_usuario))
        elif perfil_usuario == 99:
            return redirect(url_for('historial'))
    else: 
        return redirect(url_for('page_inicio'))

#Ruta para que cada usuario pueda editar su perfil para cambiar contraseña
@app.route('/edit-profile', methods=['GET', 'POST'])
def editProfile():
    form = cambioPassword(request.form)
    if 'conectado' in session:
        if session['tipo_user'] == 100:
            return render_template('public/dashboard/pages/Cat/Profile_CAT.html', dataLogin = dataLoginSesion(), form =form)
        elif session and session['tipo_user'] == 2:
            return render_template('public/dashboard/pages/Ad. Contrato/Profile_AD.html', dataLogin = dataLoginSesion(), form =form)
        elif session['tipo_user'] == 3:
            return render_template('public/dashboard/pages/Sistemas/Profile_Sistemas.html', dataLogin = dataLoginSesion(), form =form)
        elif session['tipo_user'] == 1:
            return render_template('public/dashboard/pages/Desarrollo/Profile_desarrollo.html', dataLogin = dataLoginSesion(), form =form)
        elif session['tipo_user'] == 99:
            return render_template('public/dashboard/pages/C. Trafico/Profile_CT.html', dataLogin = dataLoginSesion(), form =form)
    return redirect(url_for('inicio'))

#Ruta para que el administrador pueda modificar las cuentas a las cuales se les olvida la contraseña
@app.route('/edit-profiles-users', methods=['GET', 'POST'])
def editProfileUsers():
    form = ediotarUsuario()
    if 'conectado' in session and session['tipo_user'] == 1:
        return render_template('public/dashboard/pages/Desarrollo/Profile_users.html', dataLogin = dataLoginSesion(), form = form)
    return redirect(url_for('inicio'))     

#Ruta para observar todos los registros menos los "pendientes de aprobacion", incluso el boton de busqueda
@app.route('/historial', methods = ['GET','POST'])
def historial():
    perfil_usuario = session['tipo_user']
    form = historialForm(request.form)

    if form.validate_on_submit() and perfil_usuario in [2,3,99,100] :
        fecha_inicio_value = form.fecha_inicio.data if form.fecha_inicio.data is not None else None
        fecha_fin_value = form.fecha_fin.data if form.fecha_fin.data is not None else None
        cliente_value = form.cliente.data
        estado_value = form.estado.data
        viaje_ot_value = form.viaje_ot.data
        empresa_value = form.empresa.data
        if perfil_usuario == 100:            
            return render_template('public/dashboard/pages/Cat/historial_CAT.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(fecha_inicio_value,
                                                                                                                                                                    fecha_fin_value,
                                                                                                                                                                    cliente_value,
                                                                                                                                                                    estado_value,
                                                                                                                                                                    viaje_ot_value,
                                                                                                                                                                    empresa_value), form = form)
        if perfil_usuario == 2:
            return render_template('public/dashboard/pages/Ad. Contrato/historial_AD.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(fecha_inicio_value,
                                                                                                                                                                       fecha_fin_value,
                                                                                                                                                                       cliente_value,
                                                                                                                                                                       estado_value,
                                                                                                                                                                       viaje_ot_value, 
                                                                                                                                                                       empresa_value), form = form)
        if perfil_usuario == 99:
            return render_template('public/dashboard/pages/C. Trafico/historial_CT.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(fecha_inicio_value,
                                                                                                                                                                       fecha_fin_value,
                                                                                                                                                                       cliente_value,
                                                                                                                                                                       estado_value,
                                                                                                                                                                       viaje_ot_value, 
                                                                                                                                                                       empresa_value), form = form)
        if perfil_usuario == 3:
            return render_template('public/dashboard/pages/Sistemas/historial_Sistemas.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(fecha_inicio_value,
                                                                                                                                                                       fecha_fin_value,
                                                                                                                                                                       cliente_value,
                                                                                                                                                                       estado_value,
                                                                                                                                                                       viaje_ot_value,
                                                                                                                                                                       empresa_value), form = form)

    if 'conectado' in session and perfil_usuario in [2,3,99,100]:
        if perfil_usuario == 100:
            return render_template('public/dashboard/pages/Cat/historial_CAT.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(), form = form)
        if perfil_usuario == 2:
            return render_template('public/dashboard/pages/Ad. Contrato/historial_AD.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(), form = form)
        if perfil_usuario == 99:
            return render_template('public/dashboard/pages/C. Trafico/historial_CT.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(), form = form)
        if perfil_usuario == 3:
            return render_template('public/dashboard/pages/Sistemas/historial_Sistemas.html', dataLogin = dataLoginSesion(), data = mostrarHistorial(), form = form)
            
#Ruta para agregar un extracosto para el perfil de CAT
@app.route('/add-eecc', methods=['GET','POST'])
def addUser(): 
    form = CATForm(request.form)
    if form.validate() and dataLoginSesion()["tipoLogin"] == 100: 
        print (form.data)
        file     = request.files.get('nombre_zip') #recibiendo el archivo
        nuevoNombreFile = recibeZip(file) #Llamado la funcion que procesa la imagen
        data = form.data
        #data['dia_eecc'] = datetime.strptime(request.form['dia_eecc'], '%Y-%m-%d').strftime('%d-%m-%Y')
        data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 
        data['nombre_zip'] = nuevoNombreFile
        data['estado'] = 'Pendiente Aprobacion'
        data['hora_llegada'] = (form.hora_llegada.data).strftime('%H:%M') if form.hora_llegada.data!=None else ''  
        data['hora_salida'] = (form.hora_salida.data).strftime('%H:%M') if form.hora_llegada.data!=None else ''
        data['fecha_creacion'] = datetime.now(chile_tz).strftime('%d-%m-%Y, %H:%M')
        data['motivo'] = data['motivo_ajuste_tarifa'] + data['motivo_redestinacion'] + data['motivo_sobre_estadia'] + data['motivo_falso_flete'] + data['motivo_posicionamiento_vacio']
        data['fecha_ingreso_sitrack'] = ''
        data['fecha_ingreso_sitrack'] = ''
        data['fecha_cierre'] = ''
        data['responsable_evaluacion'] = ''
        del data['motivo_ajuste_tarifa']
        del data['motivo_redestinacion']
        del data['motivo_sobre_estadia']
        del data['motivo_falso_flete']
        del data['motivo_posicionamiento_vacio']
        del data['submit']
        del data['csrf_token']
        data['id_user'] = session['id']
        data = {key: '' if value is None else value for key, value in data.items()}

        addUserbd(data)
        return redirect(url_for('inicio'))
    
    else:
        flash(form.errors, 'danger')

    return redirect(url_for('inicio'))
  
#Ruta para ELIMINAR Registros
@app.route('/delete/<string:id>/<string:estado>')
def delete(id, estado):
    print (estado)
    if (estado == 'Pendiente Aprobacion' or estado.startswith("*Rechazado")) and  dataLoginSesion()['tipoLogin'] ==100:
        data = (id,)
        deleterow(data)
        return redirect(url_for('inicio'))

#Ruta para Descargar Registros de EECC
@app.route('/download/<string:nombre_zip>', methods=['GET'])
def download(nombre_zip):
    if 'conectado' in session and (session['tipo_user'] in [2,3,99,100]):
        dir = "static/assets/uploads/"
        # Obtener la extensión del archivo original
        _, extension = os.path.splitext(nombre_zip)
        
        # Cambiar el nombre del archivo manteniendo la extensión
        print('--------------',nombre_descarga(nombre_zip), nombre_zip)
        nuevo_nombre = 'Respaldo_viaje/ot_' + str(nombre_descarga(nombre_zip)[0]['viaje_ot']) + extension
        return send_from_directory(dir, nombre_zip, as_attachment=True, download_name = nuevo_nombre)

#Ruta para Aprobar o Rechazar un EECC
@app.route('/actualizacion', methods = ['POST'])
def actualizacion():
    if 'conectado' in session and (session['tipo_user'] == 2):
        sql = {}
        data = request.json
        print (data)
        if data['estado'] == 'Aprobado':
            sql['estado'] = data['estado']
        elif data['estado'] in ['*Rechazado', 'Rechazado']: 
            sql['estado'] = data['estado'] + ': ' + data['motivo']
        sql['responsable_evaluacion'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido']
        sql['fecha_cierre'] = datetime.now(chile_tz).strftime('%d-%m-%Y, %H:%M') 
        sql['id'] = data['id']
        values = list(sql.values())
        actualizacionEstado(values, data['estado'])
        print (values)
        return jsonify({'redirect': url_for('inicio')})
    return redirect(url_for('inicio'))

#Ruta para actualizar el estado de un por parte del rol de sistemas.
@app.route('/actualizacionSistemas/<string:id>/<string:estado>')
def actualizacionSistemas(id, estado):
    if 'conectado' in session and (session['tipo_user'] == 3):
        data = {}
        data['estado'] = estado
        data['fecha_ingreso_sitrack'] = datetime.now(chile_tz).strftime('%d-%m-%Y, %H:%M') 
        data['id'] = id
        values = list(data.values())
        actualizacionEstadoSistemas(values)      
        return redirect(url_for('inicio'))
    
#Ruta para crear usuario
@app.route('/Crear-Usuario', methods = ['GET', 'POST'])
def AdministrarUsuarios():
    if 'conectado' in session and session['tipo_user'] == 1:
        form = crearUsuario()
        print ('Ingreso a  AdministrarUsuarios 1' )
        return render_template('public/dashboard/pages/Desarrollo/Crear_Usuario.html', dataLogin = dataLoginSesion(), form = form) 
    

@app.route('/descargar_excel')
def descargar_excel():
    if 'conectado' in session:
        if session['tipo_user'] == 3:
            data = mostrarRegistros(perfil_usuario= session['tipo_user'])
            df = pd.DataFrame(data)
             # Guardar DataFrame en un objeto BytesIO (similar a un archivo en memoria)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)

            # Volver al inicio del stream
            output.seek(0)

            # Enviar archivo como respuesta
            return send_file(output, download_name="datos.xlsx", as_attachment=True)
        
        if session['tipo_user'] in [1,2,3,99,100]:
            data = todos_eecc()
            df = pd.DataFrame(data)
             # Guardar DataFrame en un objeto BytesIO (similar a un archivo en memoria)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)

            # Volver al inicio del stream
            output.seek(0)

            # Enviar archivo como respuesta
            return send_file(output, download_name="datos.xlsx", as_attachment=True)

# Cerrar session del usuario
@app.route('/logout')
def logout():
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('email', None)
    form = loginUsuario()
    flash('Cuenta cerrada con éxito', 'success')
    return render_template('public/modulo_login/index.html', form = form) 