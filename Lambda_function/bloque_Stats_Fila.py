from Simulacion.Contenedor import Contenedor
from Simulacion.Bloque import Bloque

bloque = Bloque(
    id_bloque = 1,
    maximo_x = 7,
    maximo_y = 7,
    maximo_z = 3,
    visible_dos_caras = True
)

contenedor = Contenedor(
    "AX-12", 
    "Dry", 20, 
    "Macaco", 
)

bloque.agregar_contenedor(0, 6, 0, contenedor)
bloque.agregar_contenedor(0, 6, 1, contenedor)
bloque.agregar_contenedor(0, 6, 2, contenedor)
bloque.agregar_contenedor(0, 5, 0, contenedor)
bloque.agregar_contenedor(0, 5, 1, contenedor)
bloque.agregar_contenedor(0, 5, 2, contenedor)
bloque.agregar_contenedor(0, 4, 0, contenedor)

bloque.agregar_contenedor(1, 6, 0, contenedor)
bloque.agregar_contenedor(1, 6, 1, contenedor)
bloque.agregar_contenedor(1, 6, 2, contenedor)
bloque.agregar_contenedor(1, 5, 0, contenedor)
bloque.agregar_contenedor(1, 5, 1, contenedor)
bloque.agregar_contenedor(1, 5, 2, contenedor)
bloque.agregar_contenedor(1, 4, 0, contenedor)
bloque.agregar_contenedor(1, 4, 1, contenedor)

bloque.agregar_contenedor(2, 6, 0, contenedor)
bloque.agregar_contenedor(2, 6, 1, contenedor)
bloque.agregar_contenedor(2, 6, 2, contenedor)
bloque.agregar_contenedor(2, 5, 0, contenedor)
bloque.agregar_contenedor(2, 5, 1, contenedor)
bloque.agregar_contenedor(2, 5, 2, contenedor)
bloque.agregar_contenedor(2, 4, 0, contenedor)
bloque.agregar_contenedor(2, 4, 1, contenedor)
bloque.agregar_contenedor(2, 4, 2, contenedor)

bloque.agregar_contenedor(3, 6, 0, contenedor)
bloque.agregar_contenedor(3, 6, 1, contenedor)
bloque.agregar_contenedor(3, 6, 2, contenedor)
bloque.agregar_contenedor(3, 5, 0, contenedor)
bloque.agregar_contenedor(3, 5, 1, contenedor)
bloque.agregar_contenedor(3, 5, 2, contenedor)
bloque.agregar_contenedor(3, 4, 0, contenedor)
bloque.agregar_contenedor(3, 4, 1, contenedor)

'''print(bloque.verificar_limites(4))
print(bloque.verificar_limites(5))
print(bloque.verificar_limites(6))'''

print(bloque.stats_fila())

print(bloque.ver_bloque_3d())