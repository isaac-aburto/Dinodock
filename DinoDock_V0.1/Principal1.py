from Simulacion.Contenedor import Contenedor
from Simulacion.Patio import Patio
from Simulacion.nueva_Funcion_opty import *
from datetime import datetime
import Cargar_Datos
import Estadisticas

bloques = Cargar_Datos.cargar_bloques(1)
contenedores = Cargar_Datos.cargar_contenedores(1)
bloques = Cargar_Datos.cargar_movimientos(1, bloques, contenedores)
contenedores_2 = []

patio = Patio(
    bloques = bloques
)

with open("Simulacion/Entradas2.csv", "r") as archivo:
    for i in archivo:
        line = i.strip().split(";")
        con = Contenedor(
            id_contenedor=line[0],
            marca=line[1],
            tipo=line[2],
            tamanio= line[3],
            fecha_ingreso=datetime.strptime(line[-1], '%d-%m-%Y %H:%M')
        )
        contenedores_2.append(con)

for i in range(len(contenedores_2)):
    dias_permanencia = Estadisticas.promedio_dias_marca(1, contenedores_2[i].marca)
    pos = poner_contenedor(contenedores_2[i], patio, dias_permanencia)
    print(pos)
    id_bloque = patio.find_bloque(pos[0])
    patio.bloques[id_bloque].agregar_contenedor(pos[1], pos[2], pos[3], contenedores_2[i])


for con in contenedores_2:
    conn = sacar_contenedor(con.tipo, con.marca, con.tamanio, patio)
    patio.quitar_con(conn)
    print(conn)