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


phrase ="Ma grand-mère est morte"
pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/mlp_model.pkl'
pathdialogue='D:/Documents/ENSC/GitHub/AlBidert/docs/dials/dialogue38.txt'


f= open(pathdialogue)
texte = f.read();
model = joblib.load(pathModel)
vector = stringToVect(GoogleTranslator().translate(texte))
prediction=model.predict_proba(vector.reshape(1,-1))
print(np.around(prediction,decimals=2))
# translator = GoogleTranslator()
# print("Google = "+translator.translate(phrase,lang_tgt='en'));
# print("Deepl ="+ts.deepl(phrase,to_langange='en'));
def traduction(nom_fichier_in, nom_fichier_out):
    translator = google_translator()
    # ouverture du fichier_in en lecture
    with open(path + nom_fichier_in, 'r') as file_in:
        # on récupère le contenu du fichier texte
        texte_in = file_in.read()
        nb_char = len(texte_in);
        if (nb_char%5000 == 0):
            entier = nb_char/5000;
        else :
            entier = 1+(nb_char//5000);
        print(entier);
        for i in range(entier):
            # couper le texte
            print(i);
            texte = texte_in[i*5000:((i+1)*5000)-1];
            print(texte);
            # traduction texte
            texte_out = translator.translate(texte, lang_tgt='fr')
            with open(path + nom_fichier_out, 'a',encoding='utf-8') as file_out:
                file_out.write(texte_out)

# programme principal
# path = "D:/Documents/ENSC/GitHub/AlBidert/Chatbot/"
# traduction("doctor.txt", "doctor_fr.txt")
# print("Traduction effectuée")
