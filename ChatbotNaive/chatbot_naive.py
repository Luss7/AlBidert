from google_trans_new import google_translator
import codecs
# fonctions


def intro_robot():
    print("\nBonjour. Je suis Bidert. Al Bidert, et I’ll be there for you ;)\nJe suis là pour améliorer ton humeur (si c’est possible haha)")


def intro_questionnaire():
    print("Pour cela, je vais te poser des questions et analyser tes réponses pour comprendre ton humeur.\nEnsuite je te proposerai des solutions pour que tu ailles mieux. \nPartant(e) ?")
    x = ""
    while (x != "1") and (x != "2"):
        print("Tapez 1 pour oui, 2 pour non")
        x = input()
        if x == "1":
            print("C'est parti !")
        elif x == "2":
            print("Ah. Pas grave, je le fais quand même ! (Tu peux fermer le programme si tu n’as vraiment pas envie de me parler :/ )")
        else:
            # Pas le bon nombre, il faut redemander à l'utilisateur tant qu'il n'a pas répondu 1 ou 2
            print("Je n'ai pas compris")


def intro_questionnaire_BPN():
    print("Ce questionnaire est basé sur les Basic Psychological Needs de (Deci & Ryan, 2008)")
    print("Il est composé de 21 questions et pour chacune d'elle, vous allez répondre par un chiffre de 1 à 7.")
    print("1: 'Pas vrai du tout'| 4: 'Un peu vrai' |7: 'Tout à fait vrai'")


def traduction(nom_fichier_in, nom_fichier_out):
    translator = google_translator()
    # ouverture du fichier_in en lecture
    with open(path + nom_fichier_in, 'r') as file_in:
        # on récupère le contenu du fichier texte
        texte_in = file_in.read()
        print (len(texte_in));
    # traduction texte
        texte_out = translator.translate(texte_in, lang_tgt='fr')
        with codecs.open(path + nom_fichier_out, 'w', encoding='utf-8') as file_out:
            file_out.write(texte_out)


# programme principal
path = "D:/Documents/ENSC/GitHub/AlBidert/TestChatbot/"
traduction("intents.json", "intents_fr.json")
print("Traduction effectuée")