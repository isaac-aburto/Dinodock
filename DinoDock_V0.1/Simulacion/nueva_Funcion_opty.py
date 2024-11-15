import pulp as lp


def poner_contenedor(contenedor, patio, dias_permanencia):

    #contenedores, ubicaciones, accecibilidad, dias_bloqueo, prioridad, dias_permanencia

    modelo = lp.LpProblem("Optimizacion_Entrada", lp.LpMinimize)

    ubicaciones = patio.ubicaciones_disponibles(contenedor)
    x = lp.LpVariable.dicts("x", ubicaciones, cat="Binary")

    modelo += lp.lpSum([dias_permanencia*patio.bloqueo(j)*x[j] for j in ubicaciones])


    for j in ubicaciones:
        if not patio.compatibilidad(j, contenedor):
            modelo += x[j]== 0, "compatibilidad"


    modelo.solve(lp.PULP_CBC_CMD(msg=False))

    for j in ubicaciones:
        if lp.value(x[j] == 1):
            return j
        
def sacar_contenedor(tipo, marca, tamanio, patio, peso_movimientos=1, peso_rotacion=1):

    contenedores = patio.contenedores(marca, tipo, tamanio)

    modelo = lp.LpProblem("Optimizacion_Salida", lp.LpMinimize)

    x = lp.LpVariable.dicts("x", contenedores, cat=lp.LpBinary)

    modelo += lp.lpSum([
        (peso_movimientos * patio.movimientos(j)/10 + peso_rotacion * patio.dias(j)/30) * x[j]
        for j in contenedores
    ]), "Costo_Total"

    modelo += lp.lpSum([x[c] for c in contenedores]) == 1, "Seleccion_Una_Unidad"

    modelo.solve(lp.PULP_CBC_CMD(msg=False))

    for c in contenedores:
        if x[c].value() == 1:
            return c

