
import Simulacion.Bloque as Bloque

def sacar_contenedor():

    peso_tapado = int()
    frecuencias = []
    
    pass

#? 
#TODO Pensar como poner agregar la prioridad entre frecuencias y pesos
def poner_contenedor(bloque,importancia_peso=.5, importancia_frecuencia=.5):
    frecuencias = []
        
    posicion_data =bloque.stats_fila()
    #{1: [[x,y,z], peso_tapado, frecuencias]}
    peso_min=float("inf")
    frecuencia_min=float("inf")
    mejor_posicion=[]
    for i in posicion_data:
        for posicion, peso, frecuencia in posicion_data[i]:
            if(peso <= peso_min and frecuencia <= frecuencia_min):
                peso_min = peso
                frecuencia_min = frecuencia
                mejor_posicion = posicion
    
    #TODO Poner contenedor, en el lugar con - peso tapado y tape - frecuencia
    return mejor_posicion

