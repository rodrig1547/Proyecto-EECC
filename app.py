from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)

# Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db.eecc'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'


#Rutas de la aplicación
@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM eecc")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    data = {}
    for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
                   'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 'responsable', 
                   'responsable','monto', 'estado', 'responsable_evaluacion']:
        data[field] = request.form.get(field)
    
    cursor = mysql.connection.cursor()
    columns = ', '.join([f'`{column}`' for column in data.keys()])
    placeholders = ', '.join(['%s'] * len(data))

    sql = f"INSERT INTO eecc ({columns}) VALUES ({placeholders})"
    values = list(data.values())
    print ('-------------------',values)



    cursor.execute(sql, values)
    mysql.connection.commit()

    return redirect(url_for('home'))    

@app.route('/delete/<string:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM eecc WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    data = {}
    
    for field in ['dia', 'viaje_ot', 'cliente', 'lugar', 'tipo_extra_costo', 'motivo',
               'hora_llegada', 'dia2', 'hora_salida', 'dia3', 'total_horas', 'empresa', 'responsable', 
               'monto', 'estado', 'responsable_evaluacion','usuario']:
        data[field] = request.form.get(field)
    
    print ('-------------------',data)
    data['id'] = id
    cursor = mysql.connection.cursor()
    


    sql = "UPDATE eecc SET dia = %s, viaje_ot= %s, cliente = %s, lugar = %s, tipo_extra_costo = %s, motivo = %s,\
               hora_llegada = %s, dia2 = %s, hora_salida = %s, dia3 = %s, total_horas = %s, empresa = %s, responsable = %s, \
               monto = %s, estado = %s, responsable_evaluacion = %s, usuario = %s WHERE id = %s"
    values = list(data.values())
    print ('-------------------',values)


    cursor.execute(sql, values)
    mysql.connection.commit()

    return redirect(url_for('home'))    

if __name__ == '__main__':
    app.run(debug=True, port=4000)