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
   
    name = request.json["nombre"] #debe ingresar un nombre y una contraseña
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
        "su token":str(id)} #me devuelve un token que necesitara para crear un campo de peli
        
    

@app.route('/usuario/<usuario>',methods=["GET"]) #con el nombre de usuario, te saca su reseña y calificacion, y el titulo de la pelicula
def nombre_usuario(usuario):
    reseñas = mongo.db.reseñas.find()
    
    reseñas = list(reseñas)
    pelicula = [i["pelicula"] for i in reseñas if usuario in i.values()]
    pelicula = "".join(pelicula)
    
    reseña = [i["reseña"] for i in reseñas if usuario in i.values()]
    reseña = "".join(reseña)
    
    calificacion =[i["calificacion"] for i in reseñas if usuario in i.values()]
    calificacion = "".join(calificacion)
    
    
    respuesta = {
        "pelicula": pelicula,
        "reseña": reseña,
        "calificacion":calificacion}
    c = [i for g in reseñas for k,i in g.items()]
    
    if usuario in c:
    
        return respuesta
    else:
        return {"mensaje":"usuario incorrecto o inexistente"}


@app.route('/pelicula',methods=['POST'])
def pelicula():
    pelicula = request.json["titulo"]
    token = request.json["token"]
    
    users = mongo.db.users.find()
    users = list(users)
    token = ObjectId(token)
    
    c = [i for g in users for k,i in g.items()]
    
    if token in c:
        id = mongo.db.peliculas.insert(
                {'pelicula':pelicula}
                
            )
        
        respuesta = {
                "id": str(id),
                'pelicula': pelicula
            }
        
        return {"añadido espacio de pelicula":pelicula}
        
    else:
        return {"mensaje": "token no valido"}

@app.route('/pelicula/<pelicula>',methods=["GET"]) #me saca el id de la pelicula para hacer la reseña
def id_user(pelicula):
    h = mongo.db.peliculas.find_one({'pelicula':pelicula})
    r = dumps(h["_id"])
    rjson = Response(r, mimetype="application/json")  #mimetype para que en postman me aparezca como json 
    return rjson
        
    
@app.route("/reseña",methods=["POST"]) 
def crear_reseña():
    
    usuario = request.json["usuario"]
    
    titulo = request.json["titulo"]
    reseña = request.json["reseña"]
    
    pred = preprocessing_sentence(reseña)
    pred = prediccion_reseña(pred,loaded_model)
    
    
    
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




    
        
  




