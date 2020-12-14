import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
movies = pd.read_csv("../datasets/reseñas_limpio.csv") 
y = movies['sentiment'] #NUESTRA VARIABLE Y CON 0 Y 1 PARA LAS ETIQUETAS DEL SENTIMIENTO

y = np.array(list(map(lambda x: 1 if x=="positive" else 0, y))) #CON ESTO LO QUE HAGO ES ESTABLECER EN 1 LOS POSITIVOS 
#Y EN 0 LOS NEGATIVOS.

X = movies["review"] #LA VARABLE X SERAN LAS LISTAS DE PALABRAS DE RESEÑAS

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

