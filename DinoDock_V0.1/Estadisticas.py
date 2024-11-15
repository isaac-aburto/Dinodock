from datetime import datetime
import Conexion_Bd

# OBTENER LA CANTIDAD DE CONTENDORES QUE SALEN POR MARCA, MES A MES
# MARCA, AÑO, MES, CANTIDAD
def stats_marca(dataset, fecha):
    conexion = Conexion_Bd.conexion_bd()
    stats = {}

    if (conexion):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                Marca_Contenedor, 
                YEAR(Fecha_Salida) AS Anio, 
                MONTH(Fecha_Salida) AS Mes, 
                COUNT(*) AS Cantidad_Contenedores
            FROM 
                Contenedores
            WHERE 
                Fecha_Salida IS NOT NULL
            GROUP BY 
                Marca_Contenedor, 
                YEAR(Fecha_Salida), 
                MONTH(Fecha_Salida)
            ORDER BY 
                Anio, Mes, Marca_Contenedor
        """)

        filas = cursor.fetchall()

        for fila in filas:
            if (fila[1] == fecha.year and fila[2] == fecha.month):
                stats[fila[0]] = fila[3]
    return stats
# FIN OBTENER LA CANTIDAD DE CONTENDORES QUE SALEN POR MARCA, MES A MES

# OBTENER LA CANTIDAD DE CONTENEDORES QUE SALEN POR TAMAÑO, MES A MES
# TAMAÑO, AÑO, MES, CANTIDAD
def stats_tamanio(dataset, fecha):
    conexion = Conexion_Bd.conexion_bd()
    stats = {}

    if (conexion):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                Tamaño_Contenedor, 
                YEAR(Fecha_Salida) AS Anio, 
                MONTH(Fecha_Salida) AS Mes, 
                COUNT(*) AS Cantidad_Contenedores
            FROM 
                Contenedores
            WHERE 
                Fecha_Salida IS NOT NULL
            GROUP BY 
                Tamaño_Contenedor, 
                YEAR(Fecha_Salida), 
                MONTH(Fecha_Salida)
            ORDER BY 
                Anio, Mes, Tamaño_Contenedor
        """)

        filas = cursor.fetchall()
        for fila in filas:
            if (fila[1] == fecha.year and fila[2] == fecha.month):
                tamanio = str(fila[0]) + " inch"
                stats[tamanio] = fila[3]
            
    return stats
# FIN OBTENER LA CANTIDAD DE CONTENEDORES QUE SALEN POR TAMAÑO, MES A MES

def promedio_dias_marca(dataset, marca):
    conexion = Conexion_Bd.conexion_bd()
    if (conexion):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                Marca_Contenedor,
                AVG(DATEDIFF(day, Fecha_Ingreso, Fecha_Salida)) AS promedio_dias_salida
            FROM 
                Contenedores
            WHERE 
                Fecha_ingreso IS NOT NULL and
                Fecha_salida IS NOT NULL
            GROUP BY 
                Marca_Contenedor
        """)

        filas = cursor.fetchall()
        for fila in filas:
            if fila[0] == marca:
                return fila[1]