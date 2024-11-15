from datetime import datetime
from dateutil.relativedelta import relativedelta

class Contenedor:

    def __init__(self, id_contenedor, tipo, tamanio, marca, fecha_ingreso = datetime.now(), estado = 1):
        self.id_contenedor = id_contenedor
        self.tipo = tipo
        self.tamanio = tamanio
        self.marca = marca
        self.fecha_ingreso = fecha_ingreso
        #self.fecha_salida = fecha_salida 
        self.estado = estado

    def __repr__(self):
        return (f"Contenedor(ID: {self.id_contenedor}, Tipo: {self.tipo}, Tamaño: {self.tamanio}, "
                f"Marca: {self.marca}, Fecha Ingreso: {self.fecha_ingreso}, "
                f"Estado: {self.estado})")

    def dias_en_deposito(self, fecha = datetime.now()):
        if not isinstance(fecha, datetime):
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
        diferencia =  fecha - self.fecha_ingreso

        return abs(diferencia.days)

    def dias_hasta_multa(self):
        fecha_limite = self.fecha_ingreso + relativedelta(months=3)
        diferencia = fecha_limite - datetime.now()

        return diferencia.days