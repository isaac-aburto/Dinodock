import numpy as np
import Contenedor
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Bloque:
    def __init__(self, id_bloque, maximo_x, maximo_y, maximo_z, visible_dos_caras):
        self.id_bloque = id_bloque
        self.maximo_x = maximo_x
        self.maximo_y = maximo_y
        self.maximo_z = maximo_z
        self.visible_dos_caras = visible_dos_caras #TODO por f(x,y,z) -> true/false
        self.bloque = np.zeros((maximo_x,maximo_y,maximo_z), dtype=object)

    #TODO agregar -> le falta verificar que este COMPLETAMENTE vacio atras y adelante, solo verifica el que esta a su altura
    def agregar_contenedor(self, x,y,z, contenedor):
        if(self.verificar_Existencia(x,y,z) or (not self.verificar_Existencia(x,y,z-1) and z>0) or (self.verificar_Existencia(x -1 ,y,z) and self.verificar_Existencia(x+1 ,y,z))):
            return False #? no se puede agregar
        
        self.bloque[x,y,z] = contenedor
        return True #? se agrego
    
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
            print(f'no hay nada {x, y, z, x_aux}')
            return 0
        elif (not self.verificar_Existencia(x+1,y,z) or not self.verificar_Existencia(x-1,y,z)):
            print(f'Un lado no tiene nada {x,y,z,x_aux}')
            return 1 + self.verificar_cantidad_movimientos(x,y,z + 1, x, True)
        if (x_aux != x-1 and not flag):
            print(f'avanza izquierda {x,y,z,x_aux}')
            izquierda = self.verificar_cantidad_movimientos(x - 1,y,z, x)
            print(f'izquierda: {izquierda}')
        if (x_aux != x+1 and not flag):
            print(f'avanza derecha {x,y,z,x_aux}')
            derecha = self.verificar_cantidad_movimientos(x + 1,y,z, x)
            print(f'derecha: {derecha}')
        
        print(f'fin iteracion {x,y,z,x_aux}')
        print(f'izquierda: {izquierda}')
        print(f'derecha: {derecha}')
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

    def __repr__(self):
        return (f"Bloque(Bloque: {self.id_bloque}, "
                f"Maximo X: {self.maximo_x}, Maximo Y: {self.maximo_y}, Maximo Z: {self.maximo_z}, "
                f"Visible Dos Caras: {self.visible_dos_caras})")
