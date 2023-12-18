import pyodbc

def connectionBD():
    try:
        SERVER = 'tcp:servidorpruebaseecc.database.windows.net,1433'
        DATABASE = 'excelenciaop-eecc'
        USERNAME = 'adminrodrigo'
        PASSWORD = '1234.abcd'

        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

        conn = pyodbc.connect(connectionString)
        print ('--------------Acceso correcto a BD---------------')
        return conn
    except Exception as e:
        print(f"Error en la conexión a BD: {str(e)}")
        return None
    
connectionBD()

    
    