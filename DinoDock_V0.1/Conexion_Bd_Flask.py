from flask import Flask, jsonify, request 
from Simulacion.nueva_Funcion_opty import *
from Simulacion.Patio import Patio
from Simulacion.Contenedor import Contenedor
import json
import Estadisticas
import Cargar_Datos
import Conexion_Bd



'''connectionstring = (
    "Driver={ODBC Driver 17 for SQL Server};"
    #"Server=192.168.4.113\SQLEXPRESS,10443;"
    "Server=44.213.249.107\SQLEXPRESS,10443;"
    #"Server=44.203.212.11\SQLEXPRESS,10443;"
    "Database=SITRANS_DB;"
    "UID=sa;"
    "PWD=12345678;"
    "TrustServerCertificate=yes;"
)'''

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    try:
        # Obtén los parámetros de la URL
        id_contenedor = request.args.get('id', None)
        tipo = request.args.get('tipo', None)
        marca = request.args.get('marca', None)
        tamanio = request.args.get('tamanio', None)

        # Valida que los parámetros sean proporcionados
        if not all([id_contenedor, tipo, marca, tamanio]):
            return jsonify(error="Faltan parámetros: se requieren id, tipo, marca, y tamanio."), 400

        bloques = Cargar_Datos.cargar_bloques(1)
        contenedores = Cargar_Datos.cargar_contenedores(1)
        bloques = Cargar_Datos.cargar_movimientos(1, bloques, contenedores)

        patio = Patio(bloques=bloques)

        con = Contenedor(
            id_contenedor=id_contenedor,
            tipo=tipo,
            marca=marca,
            tamanio=tamanio
        )

        dias_permanencia = Estadisticas.promedio_dias_marca(1, con.marca)
        pos = poner_contenedor(con, patio, dias_permanencia)
        id_bloque = patio.find_bloque(pos[0])
        patio.bloques[id_bloque].agregar_contenedor(pos[1], pos[2], pos[3], con)

        conexion = Conexion_Bd.conexion_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = f"INSERT INTO MOVIMIENTOS VALUES ({con.id_contenedor}, {id_bloque}, {pos[1]}, {pos[2]}, {pos[3]}, GETDATE(), 1)"
                cursor.execute(sql)
            except Exception as e:
                return jsonify(error=f"Error al insertar en la base de datos: {str(e)}"), 501

        return jsonify(id_bloque=id_bloque, posicion=pos)

    except Exception as e:
        return jsonify(error=f"Error general: {str(e)}"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

'''@app.route('/hello', methods=['GET'])
def hello():
    resultados = {}
    try:
        # Conectar a la base de datos
        with pyodbc.connect(connectionstring) as connection:
            cursor = connection.cursor()
            query = """
                SELECT 
                    Marca_Contenedor, 
                    YEAR(Fecha_Salida) AS Anio, 
                    MONTH(Fecha_Salida) AS Mes, 
                    COUNT(*) AS Cantidad_Contenedores
                FROM 
                    Contenedores
                WHERE 
                    Fecha_Salida IS NOT NULL
                GROUP BY 
                    Marca_Contenedor, 
                    YEAR(Fecha_Salida), 
                    MONTH(Fecha_Salida)
                ORDER BY 
                    Anio, Mes, Marca_Contenedor
            """
            #query = "SELECT Nombre_Cliente FROM Clientes WHERE ID_Cliente = ?"
            cursor.execute(query)
            #cursor.execute(query, (2,))
            rows = cursor.fetchall()
            #row = cursor.fetchone()

            resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

            json_data = json.dumps(resultados)

    except Exception as e:
        # Devolver un mensaje de error más detallado
        return jsonify(error=f"Error: {str(e)}"), 500

    return jsonify(message=json_data)'''

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
