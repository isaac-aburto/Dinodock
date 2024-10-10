from Bloque import Bloque
from Contenedor import Contenedor

contenedor = Contenedor(
    id_contenedor = 1,
    tipo = "seco",
    tamanio = 40,
    marca = "samsung",
    fecha_ingreso = "2024-01-01",
    estado = 1
)

bloque = Bloque(
    id_bloque = 1,
    maximo_x = 7,
    maximo_y = 7,
    maximo_z = 3,
    visible_dos_caras = True
)

bloque.ver_bloque()
print(bloque.agregar_contenedor(0, 0, 0, contenedor))
bloque.ver_bloque()