from flask import Flask, render_template, redirect, url_for, session, request
from funciones import *  #Importando mis Funciones
from Consultas_sql import *


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
        return render_template('public/modulo_login/index.html', dataPaises = listaPaises())
    
    
#Creando mi Decorador para el Home
@app.route('/')
def inicio():
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())
    else:
        return render_template('public/modulo_login/index.html', dataPaises = listaPaises())
    
    
@app.route('/login')
def login():
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin = dataLoginSesion())
    else:
        return render_template('public/modulo_login/index.html', dataPaises = listaPaises())


#Ruta para editar el perfil del cliente
@app.route('/edit-profile', methods=['GET', 'POST'])
def editProfile():
    if 'conectado' in session:
        return render_template('public/dashboard/pages/Profile.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), dataPaises = listaPaises())
    return redirect(url_for('inicio'))

#Ruta para observar los EECC.
@app.route('/EECC', methods = ['GET','POST'])

def EECC():
    if 'conectado' in session and dataLoginSesion()["tipoLogin"] == 3:
        return render_template('public/dashboard/pages/EECC_Login3.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarRegistros())
    else: 
        return render_template('public/dashboard/pages/EECC.html', dataUser = dataPerfilUsuario(), dataLogin = dataLoginSesion(), data = mostrarRegistros())


#Ruta para agregar/guardar registros a EECC
@app.route('/user', methods=['POST'])
def addUser():
    if dataLoginSesion()["tipoLogin"] == 3: 
        data = {}
        for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                    'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                    'responsable','monto','estado']:
            data[field] = request.form.get(field)
            data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 

        
    
        columns = ', '.join([f'`{column}`' for column in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        addUserbd(columns, placeholders, values)

        return redirect(url_for('EECC'))
    
    else: 
        data = {}
        for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                    'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                    'responsable','monto','estado','responsable_evaluacion']:
            data[field] = request.form.get(field)
            data['usuario'] = dataLoginSesion()['nombre'] +' ' + dataLoginSesion()['apellido'] 
    
        columns = ', '.join([f'`{column}`' for column in data.keys()])
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        addUserbd(columns, placeholders, values)

        return redirect(url_for('EECC'))
    
#Ruta para eliminar Registros
@app.route('/delete/<string:id>/<string:estado>')
def delete(id, estado): 
    data = (id,)
    deleterow(data)
    print ('-----------------------------')
    return redirect(url_for('EECC'))
   

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