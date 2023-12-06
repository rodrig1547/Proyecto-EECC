from flask import Flask, render_template, redirect, url_for, session, request, send_from_directory
from funciones import *  #Importando mis Funciones
from Consultas_sql import *
from datetime import datetime


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app


app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    else:
        return render_template('public/modulo_login/index.html')
    
    
#Creando mi Decorador para el Home
@app.route('/home')
def inicio():
    if 'conectado' in session: 
            perfil_usuario = session['tipo_user']
    if 'conectado' in session and perfil_usuario == 100:
        return render_template('public/dashboard/home_CAT.html', dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Pendiente Aprobacion'))
    elif 'conectado' in session and perfil_usuario == 2:
        return render_template('public/dashboard/home_Admin.html', dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))
    elif 'conectado' in session and perfil_usuario == 3:
        return render_template('public/dashboard/home_Sistemas.html', dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Aprobado'))
    else: 
        return render_template('public/modulo_login/index.html')

#Ruta para editar el perfil del cliente
@app.route('/edit-profile', methods=['GET', 'POST'])
def editProfile():
    if 'conectado' in session and session['tipo_user'] == 100:
        return render_template('public/dashboard/pages/Profile_CAT.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
    elif 'conectado' in session and session['tipo_user'] == 2:
        return render_template('public/dashboard/pages/Profile_AD.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
    elif 'conectado' in session and session['tipo_user'] == 3:
        return render_template('public/dashboard/pages/Profile_Sistemas.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion())
    return redirect(url_for('inicio'))     


#Ruta para observar los EECC.
@app.route('/EECC', methods = ['GET','POST'])
def EECC():
    if 'conectado' in session and 'perfil_usuario' == 'Cat':
        return render_template('public/dashboard/pages/EECC.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarRegistros('Pendiente Aprobacion'))
    return redirect(url_for('inicio'))


#Ruta para observar todos los registros, incluyendo Filtros de Busqueda.
@app.route('/historial', methods = ['GET','POST'])
def historial():
    perfil_usuario = session['tipo_user']
    if 'conectado' in session and perfil_usuario == 100:
        print (perfil_usuario)
        return render_template('public/dashboard/pages/historial_CAT.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarHistorial())
    elif 'conectado' in session and perfil_usuario == 2 :
        print (perfil_usuario)
        return render_template('public/dashboard/pages/historial_AD.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarHistorial(session['minera']))
    elif 'conectado' in session and perfil_usuario == 3 :
        print (perfil_usuario)
        return render_template('public/dashboard/pages/historial_Sistemas.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarHistorial())

       
@app.route('/historico', methods = ['GET','POST'])
def historial_historico():
    perfil_usuario = session['tipo_user']
    print ('algo', mostrarhistorico('10-11-2021', '10-11-2023'))
    if 'conectado' in session and perfil_usuario in [100, 2, 3]:
        return render_template('public/dashboard/pages/historico_Global.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarhistorico( '04-11-2023', '10-12-2023'))
    

#Ruta para agregar/guardar registros a EECC
@app.route('/user', methods=['POST'])
def addUser():
    # Si el Perfil Corresponde a CAT
    if (dataLoginSesion()["tipoLogin"] == 100) and (request.files['foto'] != ''):
        file     = request.files['foto'] #recibiendo el archivo
        nuevoNombreFile = recibeZip(file) #Llamado la funcion que procesa la imagen

        data = {}
        for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                    'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                    'responsable','monto','estado', 'nombre_zip','fecha_creacion']:
            
            data[field] = request.form.get(field)
            data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 
            data['nombre_zip'] = nuevoNombreFile
            data['estado'] = 'Pendiente Aprobacion'
            data['fecha_creacion'] = (datetime.now()).strftime('%d-%m-%Y, %H:%M')


    
        columns = ', '.join([f'`{column}`' for column in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        addUserbd(columns, placeholders, values)
        return redirect(url_for('EECC'))
    
        if(request.files['foto'] !=''):
                    file     = request.files['foto'] #recibiendo el archivo
                    nuevoNombreFile = recibeFoto(file) #Llamado la funcion que procesa la imagen
                    resultData = registrarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
                    if(resultData ==1):
                        return render_template('public/layout.html', miData = listaCarros(), msg='El Registro fue un éxito', tipo=1)
                    else:
                        return render_template('public/layout.html', msg = 'Metodo HTTP incorrecto', tipo=1)   
        else:
                    return render_template('public/layout.html', msg = 'Debe cargar una foto', tipo=1)




#Ruta para ELIMINAR Registros
@app.route('/delete/<string:id>/<string:estado>')
def delete(id, estado):
    if estado == 'Ingreso CAT' and dataLoginSesion()['tipoLogin'] ==100:
        data = (id,)
        deleterow(data)
        return redirect(url_for('EECC'))
    else: 
        data = (id,)
        deleterow(data)
        return redirect(url_for('EECC'))
    
    
#Ruta para EDITAR Registros de EECC
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    data = {}
    for field in ['dia', 'viaje_ot', 'lugar', 'tipo_extra_costo', 'motivo',
               'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 'responsable', 
               'monto', 'estado', 'responsable_evaluacion']:
        data[field] = request.form.get(field)    
    data['id'] = id
    
    print ()
    if  request.form.get('estado') == 'Aprobado' or request.form.get('estado') == 'Rechazado':
        data['responsable_evaluacion'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido']
    else: 
        data['responsable_evaluacion'] = ''
    values = list(data.values())
    editRow(values)
    return redirect(url_for('EECC'))    


#Ruta para Descargar Registros de EECC
@app.route('/download/<string:nombre_zip>', methods=['GET'])
def download(nombre_zip):
    dir = "static/assets/uploads/"
    return send_from_directory(dir, nombre_zip, as_attachment=True)

#Ruta para Aprobar o Rechazar un EECC
@app.route('/actualizacion/<string:id>/<string:estado>')
def actualizacion(id, estado):
    print(f"Received id: {id}, estado: {estado}")
    data = {}
    data['estado'] = estado
    data['responsable_evaluacion'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 
    data['fecha_cierre'] = (datetime.now()).strftime('%d-%m-%Y, %H:%M') 
    data['id'] = id
    
    values = list(data.values())
    print (values)
    actualizacionEstado(values)      
    return render_template('public/dashboard/home_Admin.html', dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Pendiente Aprobacion', session['minera']))


#Ruta para Aprobar o Rechazar un EECC
@app.route('/actualizacion/<string:id>/<string:estado>/<string:responsable>')
def actualizacionSistemas(id, estado, responsable):
    print(f"Received id: {id}, estado: {estado}")
    data = {}
    data['estado'] = estado
    data['responsable_evaluacion'] = responsable 
    data['fecha_ingreso_sitrack'] = (datetime.now()).strftime('%d-%m-%Y, %H:%M') 
    data['id'] = id
    
    values = list(data.values())
    print (values)
    actualizacionEstadoSistemas(values)      
    return render_template('public/dashboard/home_Sistemas.html', dataLogin = dataLoginSesion(), dataUser = dataPerfilUsuario(), data = mostrarRegistros('Aprobado'))

     
# Cerrar session del usuario
@app.route('/logout')
def logout():
    msgClose = ''
    # Eliminar datos de sesión, esto cerrará la sesión del usuario
    session.pop('conectado', None)
    session.pop('id', None)
    session.pop('email', None)
    msgClose ="La sesión fue cerrada correctamente"
    return render_template('public/modulo_login/index.html', msjAlert = msgClose, typeAlert=1)