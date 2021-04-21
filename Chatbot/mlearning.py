import pandas as pd
import spacy
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from google_trans_new import google_translator 

translator = google_translator();
nlp = spacy.load('en_core_web_md');
texte_in="J'ai rendez-vous demain après-midi avec un ami."
texte_out = translator.translate(texte_in, lang_tgt='en');
print(texte_out);
#-----------------Fonctions------------------#
def codageBinaire(df,colonne):
    # Codage binaire dans un nouveau DataFrame
    dummies_age = pd.get_dummies(df[colonne],prefix=colonne)

    # Concaténation du DataFrame avec les nouvelles colonnes
    df = pd.concat([df,dummies_age],axis=1)

    # Suppression de la colonne initiale
    new_df = df.drop(columns=[colonne])
    return new_df;

def vectoString(text):
    nlp = spacy.load('en_core_web_md');
    doc = nlp(text);
    return doc.vector;

# def vectoDataFrame(df,colonne):
#     return new_df;
#-----------------Programme principal-------------#
#---Charger les données---#
df_isear = pd.read_csv('ISEAR_0/isear_vector/isear_vector.csv',encoding= 'unicode_escape');

#---Nettoyer les données---#
#Codage binaire de la colonne émotion
df_isear = codageBinaire(df_isear,"Emotion");
print(df_isear);

# #Numérisation du texte : Faite avant

#Séparation des données
X= df_isear.iloc[:,0:300];
y=df_isear.iloc[:,300:307];
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40)
print(X);
print(y);
# Initialisation du modèle Regression linéaire
lr = LinearRegression()

# # Apprentissage du modèle 
prediction = lr.fit(X_train, y_train)
    
# Prédictions du modèles 
lr_prediction = lr.predict(X_test)
#print(lr_prediction)
# Score de précision Regression Lineaire
print(lr.predict(nlp(texte_out).vector.reshape(1,-1)));
print(lr.score(X_test,y_test))

#Modèle arbre de décision

clf=DecisionTreeClassifier();

prediction = clf.fit(X_train,y_train)

clf_prediction = clf.predict(X_test)
print(clf.predict(nlp(texte_out).vector.reshape(1,-1)));
print(clf.score(X_test,y_test));

#Modèle Reseau neuronne

mlp=MLPClassifier();

prediction = mlp.fit(X_train,y_train)

mlp_prediction = mlp.predict(X_test)

prediction = mlp.predict_proba(nlp(texte_out).vector.reshape(1,-1));
print(np.around(prediction,decimals=2));
print(mlp.score(X_test,y_test));

