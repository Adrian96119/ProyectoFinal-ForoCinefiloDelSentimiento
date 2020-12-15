from api.app import app 
from api.app import mongo 

from api.manipulacion_reseñas import preprocessing_sentence, prediccion_reseña

import hashlib #libreria para descifrar
from flask import request,Response
from werkzeug.security import generate_password_hash
from bson.json_util import loads, dumps, ObjectId
from api.manipulacion_reseñas import loaded_model






@app.route('/') #doy la bienvenida solo con la url original
def hola_mundo():
    return {"mensaje":"hola"}


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
        "su token":str(id)}
        
    

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

    return {"mensaje":pelicula}

@app.route('/pelicula/<pelicula>',methods=["GET"]) #me saca con el nombre el id del user
def id_user(pelicula):
    h = mongo.db.peliculas.find_one({'pelicula':pelicula})
    r = dumps(h["_id"])
    rjson = Response(r, mimetype="application/json")  #mimetype para que en postman me aparezca como json 
    return rjson
        
    
@app.route("/reseña",methods=["POST"]) 
def crear_reseña():
    
    usuario = request.json["usuario"]
    contraseña = request.json["contraseña"]
    titulo = request.json["titulo"]
    reseña = request.json["reseña"]
    
    pred = preprocessing_sentence(reseña)
    pred = prediccion_reseña(pred)
    
    
    
    peli = mongo.db.peliculas.find_one({"_id":ObjectId(titulo)})
    user = mongo.db.users.find_one({"_id":ObjectId(usuario)})

    
    id = mongo.db.reseñas.insert(
            {"pelicula": peli["pelicula"],
             "usuario": user["usuario"],
             "calificacion": pred,
            "reseña":reseña})
    
 
    
    respuesta = {
        "titulo":titulo,
        "calificacion":pred,
        "reseña": reseña
        
        }
   

    return {"RESEÑA AÑADIDA CORRECTAMENTE":respuesta }



"""
r = "Simply put, Freaky sucks."

"""
    
        
  




