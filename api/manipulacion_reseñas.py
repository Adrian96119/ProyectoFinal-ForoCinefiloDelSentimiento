from nltk.corpus import stopwords
import nltk
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import model_from_json







#cargo el modelo para meterlo en la funcion

json_file = open('api/model.json', 'r')
loaded_model_json = json_file.read()
 
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# se cargan los pesos (weights) en el nuevo modelo
loaded_model.load_weights("api/model.h5")
print("modelo cargado")





#funcion de limpieza de reseña
def preprocessing_sentence(sentence):
    stoplist = set(stopwords.words("english"))
    
    
    #quito etiquetas
    sentence = re.sub(r'<[^>]*?>', '',sentence)
    #quito signos de puntuacion
    sentence = re.sub('[^a-zA-Z]', ' ',sentence)
    #quito espacios en blanco
    sentence= re.sub(r'\s+', ' ',sentence)
    #todo minusculas
    sentence = sentence.lower()
    #quitar_string_cortos
    sentence = sentence.split()
    sentence = [x for x in sentence if len(x)>=3]
    sentence = " ".join(sentence)
    #quitar palabras irrelevantes que esten en el stopwords
    sentence = sentence.split()
    sentence = [w for w in sentence if w not in stoplist]
    #convierto sentencia a serie pandas, luego a string de lista como el formato con los que entrenó el modelo
    sentence = pd.Series(str(sentence))
    print(sentence)
  
    return sentence

#funcion que predice la reseña
def prediccion_reseña(reseña,loaded_model):
    
    
    
    
    #print("modelo cargado")
    
    movies = pd.read_csv("datasets/reseñas_limpio.csv") 
    y = movies['sentiment'] #NUESTRA VARIABLE Y CON 0 Y 1 PARA LAS ETIQUETAS DEL SENTIMIENTO

    

    X = movies["review"] #LA VARABLE X SERAN LAS LISTAS DE PALABRAS DE RESEÑAS

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)#recibira la reseña procesada y el train con el que entrene el modelo
    
    token = Tokenizer(num_words=5000) #me quedo con las 5000 palabras mas frecuences, con las que entrenó el modelo
    token.fit_on_texts(X_train) #actualizo vocabulario
    #convierto a numeros el entreno y la reseña
    X_train = token.texts_to_sequences(X_train)
    reseña = token.texts_to_sequences(reseña)
    #establezco el mismo tamaño de entrada que le meti a mi red neuronal, es decir, de una lista de 100 números.
    reseña = pad_sequences(reseña, padding='post', maxlen=100)
    #prediccion
    pred = loaded_model.predict(reseña)
    print(pred)
    if pred > 0.5:
        return ":)"
    else:
        return ":("





