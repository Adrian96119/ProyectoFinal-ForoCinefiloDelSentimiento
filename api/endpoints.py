from api.app import app
from api.app import mongo
import hashlib
from flask import request,Response
from werkzeug.security import generate_password_hash
from bson.json_util import loads, dumps




@app.route('/') #doy la bienvenida solo con la url original
def hola_mundo():
    return '<h1>BIENVENIDO AL FORO CINEFILO!!!!!!!!!!!!<h1>'


#creacion usuarios
@app.route('/usuario',methods=['POST'])
def create_user():
   
    name = request.json["nombre"]
    contraseña = request.json["contraseña"]

    
    hash = generate_password_hash(contraseña)
    id = mongo.db.users.insert(
            {'usuario':name,'contraseña':hash}
        )
    respuesta = {


            'id': str(id),
            'usuario': name,
            'contraseña': hash
    
    }

    return {
        "mensaje":"usuario creado",
        "usuario":respuesta}
        
    

@app.route('/usuario/<nombre>',methods=["GET"])
def nombre_usuario(nombre):
    usuario = mongo.db.users.find_one({'usuario':nombre})
    salida = {"usuario": usuario["usuario"],"contraseña":usuario["contraseña"]}
   
    
    return {"resultados": salida}

@app.route('/pelicula',methods=['POST'])
def pelicula():
    pelicula = request.json["titulo"]
    
    
    id = mongo.db.peliculas.insert(
        {'pelicula':pelicula}
        
    )

    respuesta = {
        "id": str(id),
        'pelicula': pelicula
    }

    return {"mensaje":f"ESPACIO DE PELICULA CREADO: {pelicula}"}
        
    
@app.route("/reseña",methods=["POST"]) 
def crear_reseña():
    usuario = request.json["usuario"]
    titulo = request.json["titulo"]
    reseña = request.json["reseña"] 

"""
from api.vocabulario_train import X_train
print(X_train)
"""



"""
r = "With its peppy cast and its brilliant, social media-hued color palette, Freaky never forgets to be anything less than a fun time."
preprocessing_sentence(r)
"""