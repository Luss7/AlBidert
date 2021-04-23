import pandas as pd
import spacy
import joblib
import os
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

#-----------------Fonctions------------------#
def codageBinaire(df,colonne):
    # Codage binaire dans un nouveau DataFrame
    dummies_age = pd.get_dummies(df[colonne],prefix=colonne)

    # Concaténation du DataFrame avec les nouvelles colonnes
    df = pd.concat([df,dummies_age],axis=1)

    # Suppression de la colonne initiale
    new_df = df.drop(columns=[colonne])
    return new_df;

def stringToVect(text):
    nlp = spacy.load('en_core_web_md');
    doc = nlp(text);
    return doc.vector;

def exportMlpLearning(fichier_csv_in,fichier_out):
    if os.path.exists(fichier_out):
        os.remove(fichier_out)
    print("Chargement des données du fichier csv...")
    #---Charger les données---#
    df_isear = pd.read_csv(fichier_csv_in,encoding= 'unicode_escape');

    print("Nettoyage des données du fichier...")
    #---Nettoyer les données---#
    #Codage binaire de la colonne émotion
    df_isear = codageBinaire(df_isear,"Emotion");

    #Séparation des données
    X= df_isear.iloc[:,0:300];
    y=df_isear.iloc[:,300:307];
    print("Separation données d'entrainement / données de test...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    #Modèle Reseau neuronne
    mlp=MLPClassifier(max_iter=1000);

    #entrainement du modele
    print("Entrainement du modèle...")
    mlp.fit(X_train,y_train);

    #Afficher le score du modèle
    print("Score du modele = "+str(mlp.score(X_test,y_test)));

    #Exportation du modele
    print("Exportation du modele...")
    joblib.dump(mlp, fichier_out)


# # Initialisation du modèle Regression linéaire
# lr = LinearRegression()

# # # Apprentissage du modèle 
# prediction = lr.fit(X_train, y_train)
    
# # Prédictions du modèles 
# lr_prediction = lr.predict(X_test)
# #print(lr_prediction)
# # Score de précision Regression Lineaire
# print(lr.predict(nlp(texte_out).vector.reshape(1,-1)));
# print(lr.score(X_test,y_test))

# #Modèle arbre de décision

# clf=DecisionTreeClassifier();

# prediction = clf.fit(X_train,y_train)

# clf_prediction = clf.predict(X_test)
# print(clf.predict(nlp(texte_out).vector.reshape(1,-1)));
# print(clf.score(X_test,y_test));






