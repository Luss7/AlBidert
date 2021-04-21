import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

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
df_isear = pd.read_csv('ISEAR_0/isear_databank/isear_clean10.csv',encoding= 'unicode_escape');
print(df_isear);

#---Nettoyer les données---#
#Codage binaire de la colonne émotion
df_isear = codageBinaire(df_isear,"Emotion");
print(df_isear);

#Numérisation du texte
# df_num = vectoDataFrame(df_isear,"Text");
df_isear["Text"]=df_isear["Text"].apply(vectoString);
# df_isear = pd.concat([df_isear,df_text],axis=1)
print(df_isear);

#Séparation des données
X=df_isear["Text"];
y=df_isear.drop(columns=["Text"]);
print(y);
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40)
# Initialisation du modèle 
lr = LinearRegression()

# Apprentissage du modèle 
prediction = lr.fit(X_train, y_train)
    
# Affichage des prédictions du modèles 
# lr_prediction = lr.predict(X_test)
# print(lr)
# # Précision Regression Lineaire
# lr.score(X_test,y_test)
# plot_confusion_matrix(lr, X_test, y_test, cmap=plt.cm.Blues)