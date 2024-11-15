from Simulacion.Contenedor import Contenedor
from Simulacion.Bloque import Bloque
from datetime import datetime
import Cargar_Datos
import Estadisticas

bloques = Cargar_Datos.cargar_bloques(123)
contenedores = Cargar_Datos.cargar_contenedores(123)
bloques = Cargar_Datos.cargar_movimientos(123, bloques, contenedores)
stats_marca = Estadisticas.stats_marca(123, datetime(2023,11,1))
marca_popular = (max(stats_marca, key=stats_marca.get),max(stats_marca.values()))

# RETONAR [BLOQUE, COORDENADAS]
def ingresar_contenedor(contenedor):
    if (contenedor.fecha_ingreso.date() == datetime.now().date()):
        bloque_min = ""
        coordenadas = ()
        peso_min = 999999
        for bloque in bloques:
            stats1 = bloque.peso_fila()
            for lista in stats1.values():
                if (lista[1] == 0):
                    if (bloque.accesible_doble):
                        return [bloque.id_bloque, (lista[0][0], lista[0][1], lista[0][2])]
                    else:
                        return [bloque.id_bloque, (lista[0][0], lista[0][1], 0)]
                else:
                    if (lista[1] < peso_min):
                        peso_min = lista[1]
                        bloque_min = bloque.id_bloque
                        coordenadas = (lista[0][0],lista[0][1],lista[0][2])
        return [bloque_min, coordenadas]
    else:
        bloque_max = ""
        coordenadas = ()
        peso_max = -1
        for bloque in bloques:
            stats1 = bloque.peso_fila()
            stats2 = bloque.marcas_fila()
            for lista in stats1.values():
                if (lista[1] > peso_max):
                    bloque_max = bloque.id_bloque
                    peso_max = lista[1]
                    coordenadas = (lista[0][0],lista[0][1],lista[0][2])
                    for marca in stats2[lista[0][0]].keys():
                        if (marca == contenedor.marca):
                            bloque_max = bloque.id_bloque
                            peso_max = lista[1]
                            coordenadas = (lista[0][0],lista[0][1],lista[0][2])

        return [bloque_max, coordenadas]

# RETORNAR [CONTENEDORES]
def egresar_contenedor(contenedor=None, id=None, marca=None, tipo=None, tamanio=None):
    if (contenedor is not None) or (id is not None):
        if (contenedor is not None):
            for bloque in bloques:
                coordenadas = bloque.ubicacion(contenedor.id_contenedor)
                if (coordenadas != [-1,-1,-1]):
                    return bloque.contenedores_previos(contenedor.id_contenedor)
                else:
                    return []
        else:
            for bloque in bloques:
                coordenadas = bloque.ubicacion(id)
                if (coordenadas != [-1,-1,-1]):
                    return bloque.contenedores_previos(id)
                else:
                    return []

    else:
        min_cant_mov = 999999
        peso_max = -1
        bloque_ideal = 0
        id_ideal = 0
        for bloque in bloques:
            for con, mov in bloque.stats_contenedores_bloque().items():
                if (marca is None or con.marca == marca) and (tipo is None or con.tipo == tipo) and (tamanio is None or con.tamanio == tamanio):
                    if (con.dias_en_deposito() > peso_max) and (mov < min_cant_mov):
                        peso_max = con.dias_en_deposito()
                        min_cant_mov = mov
                        id_ideal = con.id_contenedor
                        bloque_ideal = bloque.id_bloque
        
        for bloque in bloques:
            if (bloque.id_bloque == bloque_ideal):
                coordenadas = bloque.ubicacion(id_ideal)
                if (coordenadas != [-1,-1,-1]):
                    return bloque.contenedores_previos(id_ideal)
                else:
                    return []
            else:
                return []

def reordenar_contenedores(contenedores):
    cons_ubicacion = []
    for i in range(len(contenedores) - 1):
        cons_ubicacion.append((contenedores[i], ingresar_contenedor(contenedores[i])))
    cons_ubicacion.append((contenedores[-1], ['', (-1,-1,-1)]))
    return cons_ubicacion