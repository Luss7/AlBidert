import spacy

dir='D:/Documents/ENSC/GitHub/AlBidert/Chatbot/';
def path_to_text(path):
    with open(path, 'r') as file_in:
        # on récupère le contenu du fichier texte
        return file_in.read();

nlp = spacy.load('en_core_web_md');
doc = nlp(path_to_text(dir+'dialogue0.txt'));
print(doc.vector);
print(len(doc.vector));