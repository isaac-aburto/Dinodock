from Simulacion.Contenedor import Contenedor
from Simulacion.Bloque import Bloque
import Conexion_Bd

# CRAGAR DATOS DE BLOQUES
def cargar_bloques(dataset):
    conexion = Conexion_Bd.conexion_bd()
    bloques = []

    if (conexion):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                ROW_NUMBER() OVER (ORDER BY Bloque) AS Fila, Bloque 
            FROM 
                Movimientos 
            GROUP BY 
                Bloque
        """)

        filas = cursor.fetchall()

        for fila in filas:
            bloque = Bloque(
                id_bloque=fila[1],
                maximo_x=10,
                maximo_y=7,
                maximo_z=5,
                tipo= "Seco" if fila[0]%2!=0 else "Refrigerado",
                tamanio= 20 if fila[0]==1 else 40,
                accesible_doble= True if fila[0]%2==0 else False
            )

            bloques.append(bloque)
        
        cursor.close()
        conexion.close()
        return bloques
    
    conexion.close()
    return bloques
# FIN CRAGAR DATOS DE BLOQUES

# CARGAR DATOS DE CONTENEDORES
def cargar_contenedores(dataset):
    conexion = Conexion_Bd.conexion_bd()
    contenedores = []
    
    if (conexion):
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                * 
            FROM 
                Contenedores
        """)

        filas = cursor.fetchall()

        for fila in filas:
            contenedor = Contenedor(
                id_contenedor=fila[0],
                tipo=fila[1],
                tamanio=fila[2],
                marca=fila[3],
                fecha_ingreso=fila[4]
            )

            contenedores.append(contenedor)
        
        cursor.close()
        conexion.close()
        return contenedores
    
    conexion.close()
    return contenedores
# FIN CARGAR DATOS DE CONTENEDORES

# ASOCIACIÓN DE CONTENEDORES A SU RESPECTIVO BLOQUE
def cargar_movimientos(dataset, bloques, contenedores):
    conexion = Conexion_Bd.conexion_bd()
    cursor = conexion.cursor()

    if (conexion and bloques and contenedores):
        cursor.execute("""
            SELECT 
                Bloque, ID_Contenedor, Posicion_X, Posicion_Y, Posicion_Z 
            FROM 
                Movimientos
        """)

        filas = cursor.fetchall()

        for fila in filas:
            posicion_bloque = None
            posicion_contenedor = None
            for i, bloque in enumerate(bloques):
                if (fila[0] == bloque.id_bloque):
                    posicion_bloque = i
                    break
            
            for i, contenedor in enumerate(contenedores):
                if (fila[1] == contenedor.id_contenedor):
                    posicion_contenedor = i
                    break
            
            bloques[posicion_bloque].bloque[fila[2]-1, fila[3]-1, fila[4]-1] = contenedores[posicion_contenedor]
        
        cursor.close()
        conexion.close()
        return bloques
    
    conexion.close()
    return bloques
# FIN ASOCIACIÓN DE CONTENEDORES A SU RESPECTIVO BLOQUE