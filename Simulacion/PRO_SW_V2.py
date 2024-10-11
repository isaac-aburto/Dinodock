import pyodbc
from datetime import datetime
from dateutil.relativedelta import relativedelta

server = 'DESKTOP-NEFH690\SQLEXPRESS'
db = 'SITRANS_DB'

conexion = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={db};'
    f'Trusted_Connection=yes;'
)

cursor = conexion.cursor()

def PuntajeFechas(fecha1, fecha2):
    if fecha1 > fecha2:
        fecha1, fecha2 = fecha2, fecha1

    diferencia_relativa = relativedelta(fecha2, fecha1)
    diferencia_anos = diferencia_relativa.years
    diferencia_meses = diferencia_relativa.months
    diferencia_dias = diferencia_relativa.days

    return (diferencia_anos * 100)+(diferencia_meses * 10)+(diferencia_dias)

class Contenedor:
    def __init__(self, id_contenedor, tipo, tamanio, marca, fecha_ingreso, fecha_salida, estado):
        self.id_contenedor = id_contenedor
        self.tipo = tipo
        self.tamanio = tamanio
        self.marca = marca
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.estado = estado

    def __repr__(self):
        return (f"Contenedor(ID: {self.id_contenedor}, Tipo: {self.tipo}, Tamaño: {self.tamanio}, "
                f"Marca: {self.marca}, Fecha Ingreso: {self.fecha_ingreso}, "
                f"Fecha Salida: {self.fecha_salida}, Estado: {self.estado})")

#posicion_x = profunidad (cara obtenible)
#posicion_y = ancho
#posicion_z = altura

class Bloque:
    def __init__(self, id_contenedor, bloque, posicion_x, posicion_y, posicion_z, fecha_movimiento, usuario_responsable, maximo_x, maximo_y, maximo_z, visible_dos_caras):
        self.id_contenedor = id_contenedor
        self.bloque = bloque
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.posicion_z = posicion_z
        self.fecha_movimiento = fecha_movimiento
        self.usuario_responsable = usuario_responsable
        self.maximo_x = maximo_x
        self.maximo_y = maximo_y
        self.maximo_z = maximo_z
        self.visible_dos_caras = visible_dos_caras

    def __repr__(self):
        return (f"Bloque(Bloque: {self.bloque}, Posicion_X: {self.posicion_x}, Posicion_Y: {self.posicion_y}, "
                f"Posicion_Z: {self.posicion_z}, Fecha Movimiento: {self.fecha_movimiento}, "
                f"Usuario Responsable: {self.usuario_responsable}, "
                f"Maximo X: {self.maximo_x}, Maximo Y: {self.maximo_y}, Maximo Z: {self.maximo_z}, "
                f"Visible Dos Caras: {self.visible_dos_caras})")

#Se pueden obviar las coordenadas, pero eso implica realizar una iteración sobre la clase Bloque (doble for)
class Ponderacion:
    def __init__(self, id_contenedor, posicion_x, posicion_y, posicion_z, ponderacion):
        self.id_contenedor = id_contenedor
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.posicion_z = posicion_z
        self.ponderacion = ponderacion

    def __repr__(self):
        return (f"Ponderacion(Id_Contenedor: {self.id_contenedor}," 
                f"Posicion_X: {self.posicion_x}, Posicion_Y: {self.posicion_y}, Posicion_Z: {self.posicion_z}," 
                f"Ponderacion: {self.ponderacion})")

cursor.execute("""select
                    Con.ID_Contenedor, Tipo_Contenedor, Con.Tamaño_Contenedor, Con.Marca_Contenedor, Con.Fecha_Ingreso, Con.Fecha_Salida,
                    ECon.Estado,
                    Mov.Bloque, Mov.Posicion_X, Mov.Posicion_Y, Mov.Posicion_Z, Mov.Fecha_Movimiento, Mov.Usuario_Responsable
            from Contenedores Con
            inner join Estado_Contenedor ECon 
                    on Con.FK_Estado_Contenedor = ECon.ID_Estado_Contenedor
            inner join Movimientos Mov 
                    on Mov.ID_Contenedor = Con.ID_Contenedor
            Where
                    Con.Tamaño_Contenedor = 40""")

contenedores = []
bloques = []
ponderaciones = []

filas = cursor.fetchall()
for fila in filas:
    contenedor = Contenedor(
        id_contenedor = fila[0],
        tipo = fila[1],
        tamanio = fila[2],
        marca = fila[3],
        fecha_ingreso = fila[4].date(),
        fecha_salida = fila[5],
        estado = fila[6]
    )

    bloque = Bloque(
        id_contenedor = fila[0],
        bloque = fila[7],
        posicion_x = fila[8],
        posicion_y = fila[9],
        posicion_z = fila[10],
        fecha_movimiento = fila[11].date(),
        usuario_responsable = fila[12],
        maximo_x = 6,
        maximo_y = 6,
        maximo_z = 4,
        visible_dos_caras = True if fila[7] == "A" else False
    )

    ponderacion = Ponderacion(
        id_contenedor = fila[0],
        posicion_x = fila[8],
        posicion_y = fila[9],
        posicion_z = fila[10],
        ponderacion = PuntajeFechas(fila[11].date(), datetime.now().date())
    )
    ponderaciones.append(ponderacion)

    if len(ponderaciones) != 0:
        for ponderacion in ponderaciones:
            if ponderacion.posicion_x == fila[8] and ponderacion.posicion_y == fila[9] and ponderacion.posicion_z < fila[10]:
                ponderacion.ponderacion += PuntajeFechas(fila[11].date(), datetime.now().date())
                break

    contenedores.append(contenedor)
    bloques.append(bloque)

conexion.close()

for ponderacion in ponderaciones:
    print(ponderacion)