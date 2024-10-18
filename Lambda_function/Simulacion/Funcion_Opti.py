
import Bloque as Bloque


#ID SACAR ID
def sacar_contenedor(marca, bloque, importancia_peso=.3, importancia_movimientos=.7):

    mejorPuntaje = None
    mejorCont = None

    bloque_data = bloque.stats_contenedores_bloque()

    for i in bloque_data:
        movimientos,peso,marcaCont = bloque_data[i]
        funcionSacar = peso*importancia_peso + movimientos*importancia_movimientos
        if((mejorPuntaje == None or mejorPuntaje > funcionSacar) and marcaCont == marca):
            mejorPuntaje = funcionSacar
            mejorCont = i

    return mejorCont

#TODO Pensar como poner agregar la prioridad entre frecuencias y pesos
def poner_contenedor(bloque,importancia_peso=.4, importancia_frecuencia=.6):
        
    posicion_data = bloque.stats_fila()

    mejorPuntaje = None
    mejor_posicion=[]
    for i in posicion_data:
        posicion, peso, frecuencia = posicion_data[i]
        funcionDias = peso*importancia_peso + frecuencia*importancia_frecuencia
        if(mejorPuntaje == None or mejorPuntaje > funcionDias):
            mejorPuntaje = funcionDias
            mejor_posicion = posicion
    
    #TODO Poner contenedor, en el lugar con - peso tapado y tape - frecuencia
    return mejor_posicion


def poner_FIFO(bloque):
    
    posicion_data=bloque.stats_fila()
    mejor_peso = None
    mejor_posicion = None
    for i in posicion_data:
        posicion, peso, _ = posicion_data[i]
        if(mejor_peso == None or mejor_peso > peso):
            mejor_peso = peso
            mejor_posicion = posicion

    return mejor_posicion


def sacar_FIFO(marca,bloque):
    
    peso_alto = None
    masAntiguo = None
    bloque_data = bloque.stats_contenedores_bloque()

    for i in bloque_data:
        _,peso,marcaCont = bloque_data[i]
        if((peso_alto == None or peso_alto < peso) and marcaCont == marca):
            peso_alto = peso
            masAntiguo = i

    return masAntiguo