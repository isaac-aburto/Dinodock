import pyodbc

def conexion_bd():
    server = 'DESKTOP-NEFH690\SQLEXPRESS;'
    db = 'SITRANS_DB;'

    try:
        '''conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server}'
            f'DATABASE={db}'
            f'Trusted_Connection=yes;'
        )'''
        conexion = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            #"Server=192.168.4.113\SQLEXPRESS,10443;"
            "Server=44.213.249.107\SQLEXPRESS,10443;"
            #"Server=44.203.212.11\SQLEXPRESS,10443;"
            "Database=SITRANS_DB;"
            "UID=sa;"
            "PWD=12345678;"
            "TrustServerCertificate=yes;"
        )

        return conexion
    except Exception as e:
        print(f"Error al conectarse: {e}")
        return None