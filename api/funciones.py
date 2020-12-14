from nltk.corpus import stopwords
import nltk
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import  tomopy 
import  mkl 
mkl.domain_set_num_threads ( 1 , domain = 'fft' )



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
  
    return sentence


def prediccion_reseña(reseña,voc_train): #recibira la reseña procesada y el train con el que entrene el modelo
    
    token = Tokenizer(num_words=5000) #me quedo con las 5000 palabras mas frecuences, con las que entrenó el modelo
    token.fit_on_texts(voc_train) #actualizo vocabulario
    #convierto a numeros el entreno y la reseña
    voc_train = token.texts_to_sequences(voc_train)
    reseña = token.texts_to_sequences(reseña)
    #establezco el mismo tamaño de entrada que le meti a mi red neuronal, es decir, de una lista de 100 números.
    reseña = pad_sequences(reseña, padding='post', maxlen=100)
    #prediccion
    pred = loaded_model.predict(reseña)
    if pred > 0.5:
        print(":)")
    else:
        print(":(")
""" 
r = "With its peppy cast and its brilliant, social media-hued color palette, Freaky never forgets to be anything less than a fun time."
preprocessing_sentence(r)
"""