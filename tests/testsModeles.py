from google_trans_new import google_translator
from deep_translator import GoogleTranslator
import translators as ts
import numpy as np
import joblib
import spacy

def stringToVect(text):
    nlp = spacy.load('en_core_web_md');
    doc = nlp(text);
    return doc.vector;

def fileFrToOneVect(path):
    with open(path, encoding= 'utf-8') as f:
        texte_fr = f.read()
        texte_en = GoogleTranslator().translate(texte_fr)
        # print(texte_en);
        return stringToVect(texte_en)

def fileFrToVects(path):
    with open(path,encoding= 'utf-8') as f:
        texte_fr = f.readlines()[1:]
        vectors = []
        for line_fr in texte_fr:  
            line_en = GoogleTranslator().translate(line_fr)
            vect=stringToVect(line_en).tolist();
            vectors.append(vect);
        return vectors;



# phrase ="I don't feel very well"
pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model.pkl'
pathdialogue='D:/Documents/ENSC/GitHub/AlBidert/docs/dials/dialogue0.txt'

print("Dialogue0 : Culpabilité")
# f= open(pathdialogue)
# texte = f.read();
# vector = stringToVect(GoogleTranslator().translate(texte))
model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model prediction : ",np.around(prediction,decimals=2))

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model1.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model1 prediction : ",np.around(prediction,decimals=2))

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model2.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model2 prediction : ",np.around(prediction,decimals=2))


pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model3.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model3 prediction : ",np.around(prediction,decimals=2))


pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model4.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model4 prediction : ",np.around(prediction,decimals=2))

print("Dialogue1 : Tristesse")

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model.pkl'
pathdialogue='D:/Documents/ENSC/GitHub/AlBidert/docs/dials/dialogue1.txt'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model prediction : ",np.around(prediction,decimals=2))

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model1.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model1 prediction : ",np.around(prediction,decimals=2))

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model2.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model2 prediction : ",np.around(prediction,decimals=2))


pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model3.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model3 prediction : ",np.around(prediction,decimals=2))


pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model4.pkl'

model = joblib.load(pathModel)
vector = fileFrToOneVect(pathdialogue)
# print(vector)
prediction=model.predict_proba(vector.reshape(1,-1))[0]
print("model4 prediction : ",np.around(prediction,decimals=2))

# vector_2=stringToVect(GoogleTranslator().translate(phrase))
# prediction_2=model.predict_proba(vector_2.reshape(1,-1));
# print("prediction phrase : ",np.around(prediction_2,decimals=2))

# vectors = fileFrToVects(pathdialogue)
# # print(vectors)
# prediction_2=model.predict_proba(vectors)
# # print(prediction_2);
# tab = np.array(prediction_2)

# tab_moy = np.mean(tab, axis=0)
# list_moy = tab_moy.tolist()

# print("list2 moy around : ",np.around(list_moy,decimals=2))

# print(prediction[0]*100)

# translator = GoogleTranslator()
# print("Google = "+translator.translate(phrase,lang_tgt='en'));
# print("Deepl ="+ts.deepl(phrase,to_langange='en'));


# def traduction(nom_fichier_in, nom_fichier_out):
#     translator = google_translator()
#     # ouverture du fichier_in en lecture
#     with open(path + nom_fichier_in, 'r') as file_in:
#         # on récupère le contenu du fichier texte
#         texte_in = file_in.read()
#         nb_char = len(texte_in);
#         if (nb_char%5000 == 0):
#             entier = nb_char/5000;
#         else :
#             entier = 1+(nb_char//5000);
#         print(entier);
#         for i in range(entier):
#             # couper le texte
#             print(i);
#             texte = texte_in[i*5000:((i+1)*5000)-1];
#             print(texte);
#             # traduction texte
#             texte_out = translator.translate(texte, lang_tgt='fr')
#             with open(path + nom_fichier_out, 'a',encoding='utf-8') as file_out:
#                 file_out.write(texte_out)

# programme principal
# path = "D:/Documents/ENSC/GitHub/AlBidert/Chatbot/"
# traduction("doctor.txt", "doctor_fr.txt")
# print("Traduction effectuée")
