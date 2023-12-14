from conexionBD import *

#Creando una funcion para obtener la lista de carros.
def mostrarRegistros(perfil_usuario, cliente = None):

    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cursor = conexion_MySQLdb.cursor()
    if cliente is not None:
        cursor.execute(f"SELECT * FROM eecc Where estado = '{perfil_usuario}' and cliente = '{cliente}'  ORDER BY id DESC")
    else: cursor.execute(f"SELECT * FROM eecc Where estado = '{perfil_usuario}'  ORDER BY id DESC")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close() # Cerrando Conexion a la BD
    return insertObject

from datetime import datetime

def mostrarHistorial(dia1=None, dia2=None, cliente=None, estado=None, viaje_ot=None):
    conexion_MySQLdb = connectionBD()  # Creando mi instancia a la conexión de BD
    cursor = conexion_MySQLdb.cursor()

    # Construir la parte de la consulta con los filtros proporcionados
    where_conditions = []

    if dia1:
        where_conditions.append(f"fecha_creacion >= '{dia1}'")

    if dia2:
        where_conditions.append(f"fecha_creacion <= '{dia2}'")

    if cliente:
        where_conditions.append(f"cliente = '{cliente}'")

    if estado:
        where_conditions.append(f"estado = '{estado}'")

    # Si se proporciona el parámetro viaje_ot, ignorar todos los demás filtros
    if viaje_ot:
        cursor.execute(f"SELECT * FROM eecc WHERE viaje_ot = '{viaje_ot}' ORDER BY id DESC")
    else:
        # Si no se proporciona ningún filtro, mostrar todos los registros
        if not where_conditions :
            cursor.execute(f"SELECT * FROM eecc WHERE {(datetime.now()).strftime('%d-%m-%Y')}<=30 ORDER BY id DESC")
        else:
            # Construir la consulta completa con los filtros
            where_clause = " AND ".join(where_conditions)
            cursor.execute(f"SELECT * FROM eecc WHERE {where_clause} ORDER BY id DESC")

    myresult = cursor.fetchall()

    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()  # Cerrando conexión a la BD
    return insertObject


def mostrarhistorico(fecha_inicio, fecha_fin):
    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cursor = conexion_MySQLdb.cursor()
    cursor.execute(f"SELECT * FROM eecc WHERE STR_TO_DATE(dia, '%d-%m-%Y') AND dia >= '{fecha_inicio}' AND dia <= '{fecha_fin}' ORDER BY id DESC")


    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close() # Cerrando Conexion a la BD
    return insertObject


def addUserbd(columns, placeholders, values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = f"INSERT INTO eecc ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()

def deleterow(row):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "DELETE FROM eecc WHERE id=%s"
    cursor.execute(sql, row)
    conexion_MySQLdb.commit()
    cursor.close()

def editRow(values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "UPDATE eecc SET dia = %s, viaje_ot= %s, lugar = %s, tipo_extra_costo = %s, motivo = %s,\
               hora_llegada = %s, dia2 = %s, hora_salida = %s, dia3 = %s, total_horas = %s, empresa = %s, responsable = %s, \
               monto = %s, estado = %s, responsable_evaluacion = %s  WHERE id = %s"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()

def actualizacionEstado(values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "UPDATE eecc SET estado = %s, responsable_evaluacion = %s, fecha_cierre = %s  WHERE id = %s"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()


def actualizacionEstadoSistemas(values):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    sql = "UPDATE eecc SET estado = %s, responsable_evaluacion = %s, fecha_ingreso_sitrack = %s  WHERE id = %s"
    cursor.execute(sql, values)
    conexion_MySQLdb.commit()
    cursor.close()

def nombre_descarga(nombre_zip):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()
    cursor.execute(f"SELECT viaje_ot FROM eecc WHERE nombre_zip = '{nombre_zip}'")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close() # Cerrando Conexion a la BD
    return insertObject