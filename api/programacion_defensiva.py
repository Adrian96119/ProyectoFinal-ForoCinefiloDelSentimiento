
from api.app import app
from flask import jsonify,request

#HE GENERADO UNA SERIE DE ERRORES PARA PODER ENTENDERME CUANDO UTILICE LA API
@app.errorhandler(500)
def algo_mal(error=None):
    mensaje_error = jsonify({
    '¡ADVERTENCIA!': 'DEBES AÑADIR TODOS LOS CAMPOS O PARAMETROS, Y QUE ESTEN ESCRITOS CORRECTAMENTE!!!!',
    'TIPO DE ERROR': 500
    })
    mensaje_error.status_code = 500
    return mensaje_error


@app.errorhandler(404)
def not_found(error=None):
    mensaje_error = jsonify({
        '¡ADVERTENCIA!':'¡LA PAGINA NO SE HA ENCONTRADO PORQUE LA URL ESTA MAL INTRODUCIDA!',
        'TIPO DE ERROR': 404
    })
    mensaje_error.status_code = 404
    return mensaje_error


@app.errorhandler(405)
def metodo_erroneo(error=None):
    mensaje_error = jsonify({
        '¡ADVERTENCIA!':'UTILICE EL METODO CORRECTO... A ELEGIR = POST,GET,PUT...',
        'TIPO DE ERROR': 405
    })
    mensaje_error.status_code = 405
    return mensaje_error
    
  

@app.errorhandler(400)
def clave_inexistente(error=None):
    mensaje_error = jsonify({
        '¡ADVERTENCIA!':'¡CLAVE INEXISTENTE!',
        'TIPO DE ERROR': 400
    })
    mensaje_error.status_code = 400
    return mensaje_error