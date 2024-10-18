import pyodbc
import pandas as pd
from sqlalchemy import create_engine

def connect_to_sql_server():
    driver = 'ODBC Driver 17 for SQL Server'
    server = 'DESKTOP-NEFH690\\SQLEXPRESS'
    db = 'SITRANS_DB'
    try:
        # Conexión a la base de datos SQL Server con Windows Authentication
        '''conn = pyodbc.connect(
            f'DRIVER={driver};'
            #r'DRIVER={SQL Server};'
            #r'SERVER=GERSON\SQLEXPRESS01;'  # Reemplaza con tu servidor SQL
            f'SERVER={server};'
            f'DATABASE={db};'  # Reemplaza con tu base de datos
            'Trusted_Connection=yes;'  # Autenticación de Windows
        )'''

        connection_string = f'mssql+pyodbc:///?odbc_connect='
        connection_string += f'DRIVER={{{driver}}};SERVER={server};DATABASE={db};Trusted_Connection=yes;'

        engine = create_engine(connection_string)
        conn = engine.connect()

        return conn, 0  # Return success code
    except pyodbc.Error as e:
        print(f"Error al conectar con SQL Server: {e}")
        return None, 1  # Return error code

def fetch_container_data(conn):
    try:
        # Consulta para obtener los datos de 2023
        query = """
        SELECT Marca_Contenedor, MONTH(Fecha_Ingreso) AS Mes, COUNT(*) AS Total_Ingresos, 
               SUM(CASE WHEN Fecha_Salida IS NOT NULL THEN 1 ELSE 0 END) AS Total_Retirados
        FROM dbo.Contenedores
        WHERE YEAR(Fecha_Ingreso) = 2023
        GROUP BY Marca_Contenedor, MONTH(Fecha_Ingreso)
        """
        query = """select 
                    Marca_Contenedor, SUM(DATEDIFF(DAY, Fecha_Ingreso, Fecha_Salida)) AS Diferencia_Dias
                from 
                    Contenedores
                WHERE 
                    YEAR(Fecha_Ingreso) = 2023 AND YEAR(Fecha_Salida) = 2023
                group by 
                    Marca_Contenedor
                """
        # Leer los datos en un DataFrame de pandas
        df = pd.read_sql(query, conn)
        return df, 0  # Return success code
    except Exception as e:
        print(f"Error al ejecutar la consulta SQL: {e}")
        return None, 2  # Return error code

def calculate_probabilities(df):
    try:
        # Sumar los contenedores retirados por cada mes
        total_retirados_mes = df.groupby('Mes')['Total_Retirados'].transform('sum')
        
        # Calcular la probabilidad de retiro de cada marca en cada mes en relación al total de retirados en ese mes
        df['Probabilidad_Retiro'] = df['Total_Retirados'] / total_retirados_mes
        
        return df[['Marca_Contenedor', 'Mes', 'Probabilidad_Retiro']], 0  # Return success code
    except Exception as e:
        print(f"Error al calcular las probabilidades: {e}")
        return None, 3  # Return error code

def retirados_marca(df, marca):
    retirados_mes = df[df["Marca_Contenedor"] == marca]
    return retirados_mes,0

def main():
    # Conectar a SQL Server
    conn, conn_status = connect_to_sql_server()
    if conn_status != 0:
        return conn_status  # Error en la conexión, salir

    # Obtener los datos de contenedores
    df, fetch_status = fetch_container_data(conn)
    if fetch_status != 0:
        return fetch_status  # Error al obtener los datos, salir

    # Calcular las probabilidades
    """result_df, calc_status = calculate_probabilities(df)
    if calc_status != 0:
        return calc_status  # Error al calcular las probabilidades, salir"""
    
    result_df, calc_status = retirados_marca(df, "Xiaomi")
    if calc_status != 0:
        return calc_status  # Error al calcular las probabilidades, salir

    # Mostrar las probabilidades de retiro por marca y mes
    print(result_df)

    # Cerrar la conexión
    conn.close()
    return 0  # Éxito

if __name__ == "__main__":
    status = main()
    if status == 0:
        print("Cálculo de probabilidades completado con éxito.")
    else:
        print(f"El proceso falló con el código de error: {status}")
