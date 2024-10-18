
from Contenedor import Contenedor
from Bloque import Bloque 
import Funcion_Opti
from datetime import datetime

bloque = Bloque(
    id_bloque = 1,
    maximo_x = 7,
    maximo_y = 7,
    maximo_z = 3,
    visible_dos_caras = True
)

CARPETA_BASE ="Simulacion/contenedores{}.csv"


#! Salida -1, no encontro contenedor para ingresar

def id_contenedor(marca,entrada=True, id=0):
    
    replace = ""
    salida = -1
    with open(CARPETA_BASE.format(marca), "r") as archivo:
        if entrada:
            for i in archivo:
                if("X" not in i):
                    replace += i.strip()+" X\n"
                    salida = int(i.strip())
                else:
                    replace+=i.strip()+"\n"
        else:
            for i in archivo:
                if(str(id) in i):
                    replace += i.replace("X", "").strip()+"\n"
                else:
                    replace+=i.strip()+"\n"
    
    with open(CARPETA_BASE.format(marca), "w") as archivo:
        archivo.write(replace)

    return salida
                
    
def ingresar_contenedor(marca,funcion=Funcion_Opti.poner_FIFO):
    global bloque
    coordenadas = funcion(bloque)
    id = id_contenedor(marca)
    if id != -1:
        contenedor = Contenedor(id, "Dry", 20, marca)
        bloque.agregar_contenedor(coordenadas[0], coordenadas[1], coordenadas[2], contenedor)
        return True
    
    return False
    

def sacar_contenedor(marca, funcion=Funcion_Opti.sacar_FIFO):
    global bloque
    id = funcion(marca, bloque)
    id_contenedor(marca,False,id)
    movimientos = 0
    if id != -1 and id!=None:
        contenedor = bloque.ubicacion(id)
        movimientos = bloque.aplicar_gravedad_retirar_contenedor(contenedor[0], contenedor[1], contenedor[2])
    return movimientos


#! ARREGLA ETO POFAVO
def cargar_entrada(ruta):
    contador_movimientos = 0
    fecha_actual = None
    salida = 0
    with open(ruta, "r") as archivo: 
        for i in archivo:
            data = i.strip().split(";")
            if fecha_actual != datetime.strptime(data[2], '%d-%m-%Y %H:%M').date():
                with open("movimientos.txt", "a") as archivo:
                    archivo.write(str(fecha_actual) +";" + str(contador_movimientos) + "\n")
                fecha_actual = datetime.strptime(data[2], '%d-%m-%Y %H:%M').date()
                contador_movimientos = 0
            if data[1] == "entrada":
                salida = ingresar_contenedor(data[0])
                if salida:
                    contador_movimientos+=1
            else:
                contador_movimientos += sacar_contenedor(data[0])



print(cargar_entrada('Simulacion/Entradas.csv'))