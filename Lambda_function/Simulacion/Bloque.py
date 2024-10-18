import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#TODO CAMBIARLE EL NOMBRE A LA FUNCION verificar_posicion, REALMENTE VERIFICA QUE UNA ZONA SEA
#TODO APTA PARA PODER AGREGARLE UN CONTENEDOR SIGUIENDO UNA SERIE DE RESTRICCIONES

class Bloque:
    def __init__(self, id_bloque, maximo_x, maximo_y, maximo_z, visible_dos_caras):
        self.id_bloque = id_bloque
        self.maximo_x = maximo_x
        self.maximo_y = maximo_y
        self.maximo_z = maximo_z
        self.visible_dos_caras = visible_dos_caras #TODO por f(x,y,z) -> true/false
        self.bloque = np.zeros((maximo_x,maximo_y,maximo_z), dtype=object)

    #TODO agregar -> le falta verificar que este COMPLETAMENTE vacio atras y adelante, solo verifica el que esta a su altura
    def verificar_posicion(self, x,y,z):
        if(self.verificar_Existencia(x,y,z) or (not self.verificar_Existencia(x,y,z-1) and z>0) or (self.verificar_Existencia(x -1 ,y,z) and self.verificar_Existencia(x+1 ,y,z))):
            return False #? no se puede agregar
        
        return True #? se agrego
    
    def agregar_contenedor(self, x,y,z, contenedor):
        if(self.verificar_posicion(x,y,z)):
            self.bloque[x,y,z] = contenedor
            return True
        return False
        
    #TODO quitar
    def quitar_contenedor(self, x,y,z):
        if(not self.verificar_Existencia(x,y,z) or self.verificar_Existencia(x,y,z+1) or (self.verificar_Existencia(x -1 ,y,z) and self.verificar_Existencia(x+1 ,y,z))):
            return False #? no se puede sacar
        
        contenedor = self.bloque[x,y,z]
        self.bloque[x,y,z] = None
        return contenedor #? se saco

    #TODO verificar_Accesibilidad -> int -> cantidad movimientos
    def verificar_cantidad_movimientos(self, x,y,z, x_aux = -1, flag = False):
        izquierda = 0
        derecha = 0
        if (not self.verificar_Existencia(x,y,z)):
            return 0
        elif (not self.verificar_Existencia(x+1,y,z) or not self.verificar_Existencia(x-1,y,z)):
            return 1 + self.verificar_cantidad_movimientos(x,y,z + 1, x, True)
        if (x_aux != x-1 and not flag):
            izquierda = self.verificar_cantidad_movimientos(x - 1,y,z, x)
        if (x_aux != x+1 and not flag):
            derecha = self.verificar_cantidad_movimientos(x + 1,y,z, x)

        return 1 + self.verificar_cantidad_movimientos(x,y,z + 1, x, True) + (izquierda if izquierda <= derecha else derecha)
    
    #TODO graverdad -> true/false
    def verificar_gravedad(self, x,y,z):
        if (z == 0 or self.verificar_Existencia(x,y,z-1)):
            return True
        return False
    
    #TODO verificarExistencia
    def verificar_Existencia(self, x,y,z):
        var = False
        try:
            if(self.bloque[x,y,z]):
                var = True
        except:
            var = False
        return var

    def ver_bloque(self):
        string = ""
        for i in range(self.maximo_z):
            for j in range(self.maximo_y):
                for k in range(self.maximo_x):
                    if(self.verificar_Existencia(k,j,i)):
                        string += " 1"
                    else:
                        string += " 0"
                string += "\n"
            print()
            print(string)
            print()
            string = ""
    
    def ver_bloque_3d(self):
        matrix = np.random.rand(self.maximo_x, self.maximo_y, self.maximo_z)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        colores = ['red', 'green', 'blue']
        dx, dy, dz = 0.9, 0.9, 0.9

        for i in range(self.maximo_z):
            for j in range(self.maximo_y):
                for k in range(self.maximo_x):
                    if(self.verificar_Existencia(k,j,i)):
                        #ax.scatter(k, j, i, c='red', cmap='viridis', s=100)
                        ax.bar3d(k, j, i, dx, dy, dz, color=colores[random.randint(0, len(colores)-1)] , alpha=1)

        # Establecer los límites de los ejes para que comiencen en 1
        ax.set_xlim([0, self.maximo_x])
        ax.set_ylim([0, self.maximo_y])
        ax.set_zlim([0, self.maximo_z])

        # Etiquetas de los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Mostrar la gráfica
        plt.show()

    def verificar_limites(self,y):
        try:
            for i in range(self.maximo_x):
                if (self.verificar_Existencia(i,y,0)):
                    limite_inferior = i
                    break

            for j in range(self.maximo_x-1,-1,-1):
                if (self.verificar_Existencia(j,y,0)):
                    limite_superior = j + (1 if (not self.visible_dos_caras) else 0)
                    break
            
            #if(x >= limite_superior):
             #   return [limite_superior, limite_inferior]
        
            return [limite_inferior,limite_superior]
        except:
            return [-1,-1] #No hay contenedores en la Fila
    
    def peso_tapar_contenedor(self,x,y,z):

        if(self.verificar_posicion(x,y,z)):
            
            limite_inferior,limite_superior = self.verificar_limites(y)
            if(x >= limite_superior):
                limite_inferior,limite_superior = [limite_superior, limite_inferior]
            paso = 1 if limite_inferior < limite_superior else -1
            total_pesos = 0
            for i in range(limite_inferior, limite_superior, paso):
                for j in range(self.maximo_z):
                    if(self.verificar_Existencia(i,y,j)):
                        total_pesos+=self.bloque[i,y,j].diferencia_dias()
                    else:
                        break

            return total_pesos
        
        return -1

    #Retornar (coordenadas para colocar contenedor), peso de la fila y promedio de dias de estadía de una marca
    def stats_fila(self):
        contador = 1
        stats = {}
        frecuencia = 0
        for i in range (self.maximo_y):
            limite_inferior, limite_superior = self.verificar_limites(i)
            x,y,z = (int(self.maximo_x/2)),i,0
            peso_fila = 0
            if (limite_inferior!=-1 and limite_superior!=-1):
                for j in range (1, self.maximo_z):
                    if (not self.verificar_Existencia(limite_inferior,i,j)):
                        x,y,z = limite_inferior,i,j
                        break
                    #Verificar procedimiento para refactorizar
                    elif (not self.verificar_Existencia(limite_inferior-1,i,0)):
                        x,y,z = limite_inferior-1,i,0
                        try:
                            self.bloque[x,y,z]
                        except:
                            x,y,z = -1,-1,-1

                if (x!=-1 and y!=-1 and z!=-1):
                    peso_fila = self.peso_tapar_contenedor(x,y,z)
                    stats[contador] = [(x,y,z), peso_fila, frecuencia]
                    contador+=1
                    
                for j in range(1, self.maximo_z):
                    if (not self.verificar_Existencia(limite_superior,i,j)):
                        x,y,z = limite_superior,i,j
                        break
                    #Verificar procedimiento para refactorizar
                    elif (not self.verificar_Existencia(limite_superior+1,i,0)):
                            x,y,z = limite_superior+1,i,0
                            try:
                                self.bloque[x,y,z]
                            except:
                                x,y,z = -1,-1,-1

                if (x!=-1 and y!=-1 and z!=-1):
                    peso_fila = self.peso_tapar_contenedor(x,y,z)
                    stats[contador] = [(x,y,z), peso_fila, frecuencia]
                    contador+=1
            else:
                stats[contador] = [(x,y,z), peso_fila, frecuencia]
                contador+=1

        return stats
    
    #Retornar la cantidad de movimientos para retirar, y aplicar gravedad si aplica
    def aplicar_gravedad_retirar_contenedor(self,x,y,z):
        if (self.verificar_Existencia(x,y,z)):
            cant_mov = self.verificar_cantidad_movimientos(x,y,z)
            for i in range(z+1, self.maximo_z):
                if (self.verificar_Existencia(x,y,i)):
                    self.bloque[x,y,z] = self.bloque[x,y,i]
                    self.bloque[x,y,i] = None
            
            self.ordenar_bloque(x,y)
        
        return cant_mov
    
    def ordenar_bloque(self,x,y):
        for i in range(x+1, self.maximo_x):
            if (not self.verificar_Existencia(x,y,self.maximo_z) and self.verificar_Existencia(i,y,0)):
                for j in range(self.maximo_z-1, -1, -1):
                    if (self.verificar_Existencia(i,y,j)):
                        self.bloque[x,y,self.maximo_z-1] = self.bloque[i,y,j]

    def ubicacion(self,id):
        for x in range(self.bloque.shape[0]):
            for y in range(self.bloque.shape[1]):
                for z in range(self.bloque.shape[2]):
                    if (self.verificar_Existencia(x,y,z)):
                        contenedor = self.bloque[x, y, z]
                        if (contenedor.id_contenedor == id):
                            return [x,y,z]
        return None  # Retorna None si no se encuentra

    #Retornar Id_Contenedor, Cant Movimientos, Peso
    def stats_contenedores_bloque(self):
        stats = {}
        for x in range(self.bloque.shape[0]):
            for y in range(self.bloque.shape[1]):
                for z in range(self.bloque.shape[2]):
                    if (self.verificar_Existencia(x,y,z)):
                        contenedor = self.bloque[x,y,z]
                        stats[contenedor.id_contenedor] = [self.verificar_cantidad_movimientos(x,y,z), contenedor.diferencia_dias(), contenedor.marca]
        return stats

    def __repr__(self):
        return (f"Bloque(Bloque: {self.id_bloque}, "
                f"Maximo X: {self.maximo_x}, Maximo Y: {self.maximo_y}, Maximo Z: {self.maximo_z}, "
                f"Visible Dos Caras: {self.visible_dos_caras})")

