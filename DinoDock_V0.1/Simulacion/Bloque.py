import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Bloque:
    fecha = ""
    def __init__(self, id_bloque, maximo_x, maximo_y, maximo_z, accesible_doble, tipo, tamanio):
        self.id_bloque = id_bloque
        self.maximo_x = maximo_x
        self.maximo_y = maximo_y
        self.maximo_z = maximo_z
        self.tipo = tipo
        self.tamanio = tamanio
        self.accesible_doble = accesible_doble #TODO por f(x,y,z) -> true/false
        self.bloque = np.zeros((maximo_x,maximo_y,maximo_z), dtype=object)

    #TODO agregar -> le falta verificar que este COMPLETAMENTE vacio atras y adelante, solo verifica el que esta a su altura
    def verificar_posicion(self, x,y,z):
        if(self.verificar_existencia(x,y,z) or (not self.verificar_existencia(x,y,z-1) and z>0) or (self.verificar_existencia(x -1 ,y,z) and self.verificar_existencia(x+1 ,y,z))):
            return False #? no se puede agregar
        
        return True #? se agrego
    
    def agregar_contenedor(self, x,y,z, contenedor):
        if(self.verificar_posicion(x,y,z)):
            self.bloque[x,y,z] = contenedor
            return True
        return False
        
    #TODO quitar
    def quitar_contenedor(self, x,y,z):
        if(not self.verificar_existencia(x,y,z) or self.verificar_existencia(x,y,z+1) or (self.verificar_existencia(x -1 ,y,z) and self.verificar_existencia(x+1 ,y,z))):
            return False #? no se puede sacar
        
        contenedor = self.bloque[x,y,z]
        self.bloque[x,y,z] = None
        return contenedor #? se saco

    #TODO verificar_Accesibilidad -> int -> cantidad movimientos
    def verificar_cantidad_movimientos(self, x,y,z, x_aux = -1, flag = False):
        izquierda = 0
        derecha = 0
        if (not self.verificar_existencia(x,y,z)):
            return 0
        elif (not self.verificar_existencia(x+1,y,z) or not self.verificar_existencia(x-1,y,z)):
            return 1 + self.verificar_cantidad_movimientos(x,y,z + 1, x, True)
        if (x_aux != x-1 and not flag):
            izquierda = self.verificar_cantidad_movimientos(x - 1,y,z, x)
        if (x_aux != x+1 and not flag):
            derecha = self.verificar_cantidad_movimientos(x + 1,y,z, x)

        return 1 + self.verificar_cantidad_movimientos(x,y,z + 1, x, True) + (izquierda if izquierda <= derecha else derecha)
    
    def verificar_gravedad(self, x,y,z):
        if (z == 0 or self.verificar_existencia(x,y,z-1)):
            return True
        return False
    
    def verificar_existencia(self, x,y,z):
        var = False
        try:
            if(self.bloque[x,y,z]):
                var = True
        except:
            var = False
        return var
    
    def ver_bloque_3d(self):
        matrix = np.random.rand(self.maximo_x, self.maximo_y, self.maximo_z)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        colores = ['red', 'green', 'blue']
        dx, dy, dz = 0.9, 0.9, 0.9

        for i in range(self.maximo_z):
            for j in range(self.maximo_y):
                for k in range(self.maximo_x):
                    if(self.verificar_existencia(k,j,i)):
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
                if (self.verificar_existencia(i,y,0)):
                    limite_inferior = i
                    break

            for j in range(self.maximo_x-1,-1,-1):
                if (self.verificar_existencia(j,y,0)):
                    limite_superior = j
                    break

            return [limite_inferior,limite_superior]
        except:
            return [-1,-1] #No hay contenedores en la Fila
    
    def peso_tapar_contenedor(self,x,y,z):
        if(self.verificar_posicion(x,y,z)):
            limite_inferior,limite_superior = self.verificar_limites(y)
            if x >= limite_superior:
                limite_inferior,limite_superior = [limite_superior, limite_inferior]
            paso = 1 if limite_inferior < limite_superior else -1
            total_pesos = 0
            for i in range(limite_inferior, limite_superior, paso):
                for j in range(self.maximo_z):
                    if(self.verificar_existencia(i,y,j)):
                        total_pesos+=self.bloque[i,y,j].dias_en_deposito()
                    else:
                        break

            return total_pesos
        
        return -1

    #Retornar (coordenadas para colocar contenedor), peso de la fila
    def peso_fila(self):
        contador = 0
        stats = {}
        for i in range (self.maximo_y):
            limite_inferior, limite_superior = self.verificar_limites(i)
            x = self.maximo_x-1 if not self.accesible_doble else int(self.maximo_x/2)
            y,z = i,0
            peso_fila = 0
            if (limite_inferior!=-1 and limite_superior!=-1):
                for j in range (1, self.maximo_z):
                    if (not self.verificar_existencia(limite_inferior,i,j)):
                        x,y,z = limite_inferior,i,j
                        break
                    #Verificar procedimiento para refactorizar
                    elif (not self.verificar_existencia(limite_inferior-1,i,0)):
                        x,y,z = limite_inferior-1,i,0
                        try:
                            self.bloque[x,y,z]
                        except:
                            x,y,z = -1,-1,-1

                if (x!=-1 and y!=-1 and z!=-1):
                    peso_fila = self.peso_tapar_contenedor(x,y,z)
                    stats[contador] = [(x,y,z), peso_fila]
                    contador += 1
                    
                for j in range(1, self.maximo_z):
                    if (not self.verificar_existencia(limite_superior,i,j)):
                        x,y,z = limite_superior,i,j
                        break
                    #Verificar procedimiento para refactorizar
                    elif (not self.verificar_existencia(limite_superior+1,i,0)):
                            x,y,z = limite_superior+1,i,0
                            try:
                                self.bloque[x,y,z]
                            except:
                                x,y,z = -1,-1,-1

                if (x!=-1 and y!=-1 and z!=-1) and (self.accesible_doble):
                    peso_fila = self.peso_tapar_contenedor(x,y,z)
                    stats[contador] = [(x,y,z), peso_fila]
                    contador += 1
            else:
                stats[contador] = [(x,y,z), peso_fila]
                contador += 1

        return stats
    
    #Retornar la cantidad de movimientos para retirar, y aplicar gravedad si aplica
    def aplicar_gravedad_retirar_contenedor(self,x,y,z):
        if (self.verificar_existencia(x,y,z)):
            for i in range(z+1, self.maximo_z):
                if (self.verificar_existencia(x,y,i)):
                    self.bloque[x,y,z] = self.bloque[x,y,i]
                    self.bloque[x,y,i] = None
                else:
                    self.bloque[x,y,z] = None
            self.ordenar_bloque(x,y)
        
        return 1
    
    def ordenar_bloque(self,x,y):
        for i in range(x+1, self.maximo_x):
            if (not self.verificar_existencia(x,y,self.maximo_z-1) and self.verificar_existencia(i,y,0)):
                for j in range(self.maximo_z-1, -1, -1):
                    if (self.verificar_existencia(i,y,j)):
                        self.bloque[x,y,self.maximo_z-1] = self.bloque[i,y,j]

    def ubicacion(self,id):
        for x in range(self.bloque.shape[0]):
            for y in range(self.bloque.shape[1]):
                for z in range(self.bloque.shape[2]):
                    if (self.verificar_existencia(x,y,z)):
                        contenedor = self.bloque[x, y, z]
                        if (contenedor.id_contenedor == id):
                            return [x,y,z]
        return [-1,-1,-1]  # Retorna [-1,-1,-1] si no se encuentra

    #Retornar {Contenedor: Cant Movimientos}
    def stats_contenedores_bloque(self):
        stats = {}
        for x in range(self.bloque.shape[0]):
            for y in range(self.bloque.shape[1]):
                for z in range(self.bloque.shape[2]):
                    if (self.verificar_existencia(x,y,z)):
                        contenedor = self.bloque[x,y,z]
                        stats[contenedor] = self.verificar_cantidad_movimientos(x,y,z)
        return stats
    
    # RETORNAR FILA: [MARCA, CANT. DE CONTENEDORES]
    def marcas_fila(self):
        stats = {}
        for i in range(self.maximo_y):
            marcas = {}
            limite_inferior, limite_superior = self.verificar_limites(i)
            if (limite_inferior != -1 and limite_superior != -1):
                '''if (limite_inferior > limite_superior):
                    limite_inferior, limite_superior = [limite_superior, limite_inferior]'''
                for j in range(limite_inferior, limite_superior+1):
                    for k in range(self.maximo_z):
                        if (self.verificar_existencia(i,j,k)):
                            if (self.bloque[i,j,k].marca in marcas):
                                marcas[self.bloque[i,j,k].marca] += 1
                            else:
                                marcas[self.bloque[i,j,k].marca] = 1
                
                stats[i] = marcas
            else:
                stats[i] = {"Marca": 0}

        return stats
    
    def contenedores_previos(self, id):
        print(f'tipo id: {type(id)}')
        cons_salen = []
        pos_x, pos_y, pos_z = self.ubicacion(id)
        print(f'ubicacion id: {self.ubicacion(id)}')
        print(f'ubicacion id directa: {self.ubicacion(5)}')
        if (pos_x != -1 and pos_y != -1 and pos_z != -1):
            limite_inferior, limite_superior = self.verificar_limites(pos_y)
            if (self.accesible_doble):
                cerca_limite_inferior = abs(pos_x - limite_inferior)
                cerca_limite_superior = abs(pos_x - limite_superior)
                if (cerca_limite_inferior < cerca_limite_superior):
                    for i in range(limite_inferior, pos_x+1):
                        for j in range(self.maximo_z-1, -1, -1):
                            if (self.verificar_existencia(i, pos_y, j)):
                                cons_salen.append(self.bloque[i, pos_y, j])
                else:
                    for i in range(limite_superior, pos_x-1, -1):
                        for j in range(self.maximo_z-1, -1, -1):
                            if (self.verificar_existencia(i, pos_y, j)):
                                cons_salen.append(self.bloque[i, pos_y, j])
            else:
                for i in range(limite_inferior, pos_x+1):
                    for j in range(self.maximo_z-1, -1, -1):
                        if (self.verificar_existencia(i, pos_y, j)):
                            cons_salen.append(self.bloque[i, pos_y, j])
        
        return cons_salen

    def __repr__(self):
        return (f"Bloque(Bloque: {self.id_bloque}, "
                f"Maximo X: {self.maximo_x}, Maximo Y: {self.maximo_y}, Maximo Z: {self.maximo_z}, "
                f"Tipo: {self.tipo}, "
                f"Tamaño: {self.tamanio}, "
                f"Visible Dos Caras: {self.accesible_doble})")

