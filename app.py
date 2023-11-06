from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from config import config
from controller.controllerCarro import *

app = Flask(__name__)

#Rutas de la aplicación
@app.route('/home')
def home():
    return render_template('index.html', data= mostrarRegistros())

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    data = {}
    for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                   'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 
                   'responsable','monto', 'estado', 'responsable_evaluacion']:
        data[field] = request.form.get(field)
    
   
    columns = ', '.join([f'`{column}`' for column in data.keys()])
    placeholders = ', '.join(['%s'] * len(data))
    values = list(data.values())
    addUserbd(columns, placeholders, values)

    return redirect(url_for('home'))    
#Ruta para eliminar Registros
@app.route('/delete/<string:id>')
def delete(id):
    data = (id,)
    deleterow(data)
    return redirect(url_for('home'))

#Ruta para Editar Registros
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    data = {}
    
    for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
               'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 'responsable', 
               'monto', 'estado', 'responsable_evaluacion','usuario']:
        data[field] = request.form.get(field)    
    data['id'] = id
    values = list(data.values())
    editRow(values)
    return redirect(url_for('home'))    

if __name__ == '__main__':
    app.run(debug=True, port=4000)