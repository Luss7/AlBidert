import spacy
from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             DeepL,
                             QCRI,
                             single_detection,
                             batch_detection)
from google_trans_new import google_translator
transaltor = google_translator();
print(transaltor.translate("Tell me more about thour exams?",lang_tgt='fr'));
# print(GoogleTranslator(source='auto', traget='en').translate("Bof bof... ")); 
def vectorisation(dir,nomFichier):
    text = path_to_text(dir+nomFichier);
    doc = nlp(text);
    vecteur = doc.vector;
    return vecteur;

dir='D:/Documents/ENSC/GitHub/AlBidert/Chatbot/';

def path_to_text(path):
    with open(path, 'r') as file_in:
        # on récupère le contenu du fichier texte
        return file_in.read();

# nlp = spacy.load('en_core_web_md');
# doc = nlp(path_to_text(dir+'dialogue1.txt'));
# print(doc.vector);
# print(len(doc.vector));

# vecteur = vectorisation(dir,'dialogue1.txt');
# print(vecteur);


