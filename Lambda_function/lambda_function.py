import Simulacion.Contenedor as Contenedor

import json

def lambda_handler(event, context):
    # TODO implement
    # TODO LA SIMULACION jeje

    bloque = bloque(
        id_bloque = 1,
        maximo_x = 7,
        maximo_y = 7,
        maximo_z = 3,
        visible_dos_caras = True
    )

    return {
        'statusCode': 200,
        'body': json.dumps(bloque)
    }


