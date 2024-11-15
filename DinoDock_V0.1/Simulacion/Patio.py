

class Patio:

    def __init__(self, bloques):
        self.bloques = bloques

    def bloqueo(self, ubicacion):
        return self.bloques[self.find_bloque(ubicacion[0])].peso_tapar_contenedor(ubicacion[1],ubicacion[2],ubicacion[3])
        

    def compatibilidad(self, ubicacion, contenedor):

        if (self.bloques[self.find_bloque(ubicacion[0])].tipo == contenedor.tipo):
            return True
        elif (self.bloques[self.find_bloque(ubicacion[0])].tamanio == contenedor.tamanio) and (contenedor.tipo != "Refrigerado"):
            return True
        else:
            return False

    def ubicaciones_disponibles(self, contenedor):
        
        salida = []
        for i in self.bloques:
            if (i.tipo == contenedor.tipo) and (int(i.tamanio) == int(contenedor.tamanio)):
                for value in i.peso_fila().values():
                    posicion = (ord(i.id_bloque), value[0][0], value[0][1], value[0][2])
                    salida.append(posicion)

        return salida
    
    def find_bloque(self, id):
        id = chr(id)
        for i in range(len(self.bloques)):
            if (id == self.bloques[i].id_bloque):
                return i
        return -1
    
    def contenedores(self, marca, tipo, tamanio):
        salidas = []
        for bloque in self.bloques:
            if (bloque.tipo == tipo) and (int(bloque.tamanio) == int(tamanio)):
                for con, mov in bloque.stats_contenedores_bloque().items():
                    if (marca is None or con.marca == marca) and (tipo is None or con.tipo == tipo) and (tamanio is None or int(con.tamanio) == int(tamanio)):
                        salidas.append(con)
        return salidas
    
    def movimientos(self, contenedor):
        for bloque in self.bloques:
            x,y,z = bloque.ubicacion(contenedor.id_contenedor)
            if (x != -1):
                return bloque.verificar_cantidad_movimientos(x,y,z)
        return 0
    
    def dias(self, contenedor):
        return contenedor.dias_en_deposito()
    
    def quitar_con(self, contenedor):
        for bloque in self.bloques:
            x,y,z = bloque.ubicacion(contenedor.id_contenedor)
            bloque.aplicar_gravedad_retirar_contenedor(x,y,z)
            print(bloque.ver_bloque_3d())