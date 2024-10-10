from Contenedor import Contenedor
from datetime import datetime

c = Contenedor("AX-12", "Dry", 20, "Macaco", datetime(2024, 8, 5))

print(c.diferencia_dias())
print(c.multa())
print(c.multa())
print(c.fecha_ingreso)
