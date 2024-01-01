from conexionBD import *
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash



def consultaCuentaExistente(email):
    """
        El usuario al tratar de ingresar se deben corrobarar sus credenciales.
    """
    conexion_SQLServer = connectionBD()
    cursor = conexion_SQLServer.cursor()
    cursor.execute("SELECT * FROM login WHERE email = ?", [email])
    columns = [column[0] for column in cursor.description]
    resultado = [dict(zip(columns, row)) for row in cursor.fetchall()][0]
    return resultado 


def verificar_contrasena_actual(id, contrasena):
    conexion_SQLServer = connectionBD()
    cursor = conexion_SQLServer.cursor()

    # Consulta SQL para obtener la contraseña almacenada en la base de datos
    cursor.execute("SELECT password FROM login WHERE id = ?", [id])
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[0], contrasena):
        # La contraseña es correcta
        return True
    else:
        # La contraseña no es correcta o no se encontró el usuario
        return False


def mostrarRegistros(perfil_usuario, cliente:list = None, id_user: int = None):
    try:
        conexion_SQLServer = connectionBD()
        cursor = conexion_SQLServer.cursor()
        if perfil_usuario == 2:
            placeholders = ', '.join(['?'] * len(cliente))
            query = f"SELECT * FROM extracostos WHERE estado = 'Pendiente Aprobacion' AND cliente IN ({placeholders}) ORDER BY id DESC"
            
            cursor.execute(query, *cliente)
        elif perfil_usuario == 3:
            cursor.execute ("""SELECT * FROM extracostos 
                            WHERE estado = 'Aprobado' 
                            ORDER BY id DESC""")

        elif perfil_usuario == 100:
            cursor.execute (f"""SELECT *, FORMAT(dia_eecc, 'dd-MM-yyyy') AS dia_eecc 
                            FROM extracostos WHERE (estado = 'Pendiente Aprobacion' or estado LIKE '*Rechazado%') and id_user = {id_user} 
                            ORDER BY id DESC""")

        myresult = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        insert_object = [dict(zip(column_names, record)) for record in myresult]
        return insert_object
    except Exception as e:
        # Manejar la excepción según tus necesidades
        print(f"Error: {e}")
        return None

def mostrarHistorial(dia1=None, dia2=None, cliente=None, estado=None, viaje_ot=None, empresa=None):
    conexion_SQLServer = connectionBD()  # Creando mi instancia a la conexión de BD
    cursor = conexion_SQLServer.cursor()

    # Construir la parte de la consulta con los filtros proporcionados
    where_conditions = []

    if dia1:
        where_conditions.append(f"dia_eecc >= '{dia1}'")

    if dia2:
        where_conditions.append(f"dia_eecc <= '{dia2}'")

    if cliente:
        where_conditions.append(f"cliente = '{cliente}'")

    if estado:
        where_conditions.append(f"estado LIKE '{estado}'")

    if empresa:
        where_conditions.append(f"empresa = '{empresa}'")

    # Si se proporciona el parámetro viaje_ot, ignorar todos los demás filtros
    if viaje_ot:
        cursor.execute(f"SELECT *, FORMAT(dia_eecc, 'dd-MM-yyyy') AS dia_eecc  FROM extracostos WHERE viaje_ot = '{viaje_ot}' ORDER BY id DESC")
    else:
        # Si no se proporciona ningún filtro, mostrar todos los registros
        if not where_conditions:
            fecha_actual = ((datetime.now())-timedelta(days=30)).strftime('%Y-%m-%d')
            print (fecha_actual)
            query = f"""SELECT *, FORMAT(dia_eecc, 'dd-MM-yyyy') as dia_eecc 
                        FROM extracostos 
                        WHERE dia_eecc > ? ORDER BY id DESC
                        """
            cursor.execute(query, fecha_actual)
        else:
            # Construir la consulta completa con los filtros
            where_clause = " AND ".join(where_conditions)
            cursor.execute(f"SELECT * ,FORMAT(dia_eecc, 'dd-MM-yyyy') AS dia_eecc  FROM extracostos WHERE {where_clause} ORDER BY id DESC")

    myresult = cursor.fetchall()

    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()  # Cerrando conexión a la BD
    return insertObject

def addUserbd(data):
    conexion_SQLServer = connectionBD()
    
    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()

            columns = ', '.join([f'[{column}]' for column in data.keys()])
            placeholders = ', '.join(['?'] * len(data))
            
            # Asegúrate de tener la consulta SQL adecuada aquí
            sql = f"INSERT INTO extracostos ({columns}) VALUES ({placeholders})"
            
            values = list(data.values())
            
            cursor.execute(sql, values)
            conexion_SQLServer.commit()
            cursor.close()  # Cerrando el cursor
        except Exception as e:
            print(f"Error al insertar datos en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")

def deleterow(id):
    conexion_SQLServer = connectionBD()

    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()

            sql = "DELETE FROM extracostos WHERE id = ?"
            cursor.execute(sql, id)
            conexion_SQLServer.commit()
            cursor.close()  # Cerrando el cursor
        except Exception as e:
            print(f"Error al eliminar registro en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")


def actualizacionEstado(values, estado):
    conexion_SQLServer = connectionBD()

    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()
            if estado in ['Aprobado', '*Rechazado', 'Rechazado'] :
                sql = """
                    UPDATE extracostos
                    SET
                        estado = ?,
                        responsable_evaluacion = ?,
                        fecha_cierre = ?
                    WHERE id = ?
                """
                # Reemplaza "nombre_de_tabla" con el nombre real de tu tabla en SQL Server
                cursor.execute(sql, values)                
                conexion_SQLServer.commit()

            cursor.close()  # Cerrando el cursor
        except Exception as e:
            print(f"Error al actualizar el estado en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")



def actualizacionEstadoSistemas(values):
    conexion_SQLServer = connectionBD()

    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()

            sql = """
                UPDATE extracostos
                SET
                    estado = ?,
                    fecha_ingreso_sitrack = ?
                WHERE id = ?
            """
            
            # Reemplaza "nombre_de_tabla" con el nombre real de tu tabla en SQL Server
            cursor.execute(sql, values)
            
            conexion_SQLServer.commit()
            cursor.close()  # Cerrando el cursor
        except Exception as e:
            print(f"Error al actualizar el estado en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")

def nombre_descarga(nombre_zip):
    conexion_SQLServer = connectionBD()
    
    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()

            # Utiliza parámetros para evitar SQL injection
            cursor.execute("SELECT viaje_ot FROM extracostos WHERE nombre_zip = ?", nombre_zip)
            
            myresult = cursor.fetchall()

            # Convertir los datos a un diccionario
            insertObject = []
            columnNames = [column[0] for column in cursor.description]
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))

            cursor.close()  # Cerrando conexión a la BD
            return insertObject
        except Exception as e:
            print(f"Error al insertar datos en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")


def actualizar_password_sql_server(nueva_password, id):
    conexion_SQLServer = connectionBD()

    if conexion_SQLServer:
        try:
            cursor = conexion_SQLServer.cursor()

            sql = """
                UPDATE login  
                SET                              
                    password = ?
                WHERE id = ?
            """
            
            # Reemplaza "nombre_de_tabla" con el nombre real de tu tabla en SQL Server
            cursor.execute(sql, nueva_password, id)
        
            conexion_SQLServer.commit()
            cursor.close()  # Cerrando el cursor
        except Exception as e:
            print(f"Error al actualizar la contraseña en la base de datos: {str(e)}")
        finally:
            conexion_SQLServer.close()  # Cerrando la conexión a la BD
    else:
        print("No se pudo establecer conexión con la base de datos.")


def maestro(minera):
    if minera =='minera':
        try:
            conexion_SQLServer = connectionBD()
            cursor = conexion_SQLServer.cursor()
            cursor.execute (f"SELECT * FROM maestro_minera ORDER BY  minera ASC")
            myresult = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            insert_object = [dict(zip(column_names, record)) for record in myresult]
            return insert_object
        except Exception as e:
            # Manejar la excepción según tus necesidades
            print(f"Error: {e}")
            return None
    elif minera == 'empresa':
        try:
            conexion_SQLServer = connectionBD()
            cursor = conexion_SQLServer.cursor()
            cursor.execute (f"SELECT * FROM maestro_empresa ORDER BY  empresa ASC")
            myresult = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            insert_object = [dict(zip(column_names, record)) for record in myresult]
            return insert_object
        except Exception as e:
            # Manejar la excepción según tus necesidades
            print(f"Error: {e}")
            return None

def todos_eecc():
    conexion_SQLServer = connectionBD()
    cursor = conexion_SQLServer.cursor()
    query = ("""SELECT id as ID,
                              usuario AS Usuario,
                              dia_eecc as 'Dia EECC',
                            viaje_ot AS 'Viaje/OT',
                            cliente AS Cliente,
                            agencia AS Agencia,
                            tipo_extra_costo AS 'Tipo Extra Costo',
                            motivo AS Motivo, 
                            hora_llegada AS 'Hora Llegada', 
                            dia2 as Dia,
                            hora_salida AS Hora_Salida,
                            dia3 AS Dia,
                            empresa AS Empresa,
                            monto AS Monto,
                            estado AS Estado,
                            responsable_evaluacion AS 'Responsable Evaluacion',
                            fecha_creacion AS 'Fecha Creacion',
                            fecha_cierre AS 'Fecha Cierre',
                            fecha_ingreso_sitrack AS 'Ingreso Sitrack'
                              
                    FROM extracostos 
                    ORDER BY id DESC
                    """)
    cursor.execute(query)
    myresult = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    insert_object = [dict(zip(column_names, record)) for record in myresult]
    return insert_object