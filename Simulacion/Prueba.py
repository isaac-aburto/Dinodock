import numpy as np
import matplotlib.pyplot as plt
from Contenedor import Contenedor
from Bloque import Bloque
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import random

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
    datetime(2024, 8, 5)
)

print(bloque.agregar_contenedor(0, 6, 0, contenedor))
print(bloque.agregar_contenedor(0, 6, 1, contenedor))
print(bloque.agregar_contenedor(0, 6, 2, contenedor))
print(bloque.agregar_contenedor(0, 5, 0, contenedor))
print(bloque.agregar_contenedor(0, 5, 1, contenedor))
print(bloque.agregar_contenedor(0, 5, 2, contenedor))
print(bloque.agregar_contenedor(0, 4, 0, contenedor))

print(bloque.agregar_contenedor(1, 6, 0, contenedor))
print(bloque.agregar_contenedor(1, 6, 1, contenedor))
print(bloque.agregar_contenedor(1, 6, 2, contenedor))
print(bloque.agregar_contenedor(1, 5, 0, contenedor))
print(bloque.agregar_contenedor(1, 5, 1, contenedor))
print(bloque.agregar_contenedor(1, 5, 2, contenedor))
print(bloque.agregar_contenedor(1, 4, 0, contenedor))
print(bloque.agregar_contenedor(1, 4, 1, contenedor))

print(bloque.agregar_contenedor(2, 6, 0, contenedor))
print(bloque.agregar_contenedor(2, 6, 1, contenedor))
print(bloque.agregar_contenedor(2, 6, 2, contenedor))
print(bloque.agregar_contenedor(2, 5, 0, contenedor))
print(bloque.agregar_contenedor(2, 5, 1, contenedor))
print(bloque.agregar_contenedor(2, 5, 2, contenedor))
print(bloque.agregar_contenedor(2, 4, 0, contenedor))
print(bloque.agregar_contenedor(2, 4, 1, contenedor))
print(bloque.agregar_contenedor(2, 4, 2, contenedor))

print(bloque.agregar_contenedor(3, 6, 0, contenedor))
print(bloque.agregar_contenedor(3, 6, 1, contenedor))
print(bloque.agregar_contenedor(3, 6, 2, contenedor))
print(bloque.agregar_contenedor(3, 5, 0, contenedor))
print(bloque.agregar_contenedor(3, 5, 1, contenedor))
print(bloque.agregar_contenedor(3, 5, 2, contenedor))
print(bloque.agregar_contenedor(3, 4, 0, contenedor))
print(bloque.agregar_contenedor(3, 4, 1, contenedor))



# Crear una matriz 3x3x3 con valores de ejemplo
matrix = np.random.rand(bloque.maximo_x, bloque.maximo_y, bloque.maximo_z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Crear una malla de coordenadas
#x, y, z = np.indices(matrix.shape)}

colores = ['red', 'green', 'blue']

dx, dy, dz = 0.9, 0.9, 0.9

for i in range(bloque.maximo_z):
    for j in range(bloque.maximo_y):
        for k in range(bloque.maximo_x):
            if(bloque.verificar_Existencia(k,j,i)):
                #ax.scatter(k, j, i, c='red', cmap='viridis', s=100)
                ax.bar3d(k, j, i, dx, dy, dz, color=colores[random.randint(0, len(colores)-1)] , alpha=1)

# Graficar los valores de la matriz en 3D
#ax.scatter(x, y, z, c=matrix.flatten(), cmap='viridis', s=100)

# Establecer los límites de los ejes para que comiencen en 1
ax.set_xlim([0, bloque.maximo_x])
ax.set_ylim([0, bloque.maximo_y])
ax.set_zlim([0, bloque.maximo_z])

# Etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar la gráfica
plt.show()
