from Simulacion.Contenedor import Contenedor
from datetime import datetime
import Optimizacion_1

def ingresar_contenedor(contenedor):
    if isinstance(contenedor, Contenedor.__class__):
        pos_optima = Optimizacion_1.ingresar_contenedor(contenedor)
        for bloque in Optimizacion_1.bloques:
            if (bloque.id_bloque == pos_optima[0]):
                bloque.agregar_contenedor(pos_optima[1][0], pos_optima[1][1], pos_optima[1][2])
                return True
    else:
        return False
    
def egresar_contenedor(contenedor=None, id=None, marca=None, tipo=None, tamanio=None):
    if isinstance(contenedor, Contenedor.__class__):
        cons_salen = Optimizacion_1.egresar_contenedor(contenedor, id, marca, tipo, tamanio)
    else:
        return 

def reordenar_contenedores(contenedores):
    cons_ubicacion = []
    for i in range(len(contenedores) - 1):
        cons_ubicacion.append((contenedores[i], ingresar_contenedor(contenedores[i])))
    cons_ubicacion.append((contenedores[-1], ['', (-1,-1,-1)]))
    return cons_ubicacion

con1 = Contenedor(
    id_contenedor=123,
    tipo="Seco",
    tamanio=40,
    marca="Samsung",
    fecha_ingreso=datetime(2024,1,1)
)

con2 = Contenedor(
    id_contenedor=1,
    tipo="Seco",
    tamanio=20,
    marca="Evergreen",
    fecha_ingreso=datetime(2024,8,1,8,0,0)
)

id = 5
id = 1
marca = "Maersk"
tamanio = 40
tipo = "Seco"