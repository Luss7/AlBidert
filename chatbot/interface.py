#! /Program/Python/python37
# coding: utf-8
# interface.py

import os
from deep_translator import GoogleTranslator
from eliza import Eliza
from eliza import write_in_file
from eliza import pathdoctor
from eliza import pathdialogue
import tkinter as tk
import joblib
import spacy
import numpy as np

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model.pkl'

def stringToVect(text):
    nlp = spacy.load('en_core_web_md');
    doc = nlp(text);
    return doc.vector;

# import tkinter.ttk as ttk
# import tkinter.scrolledtext as ScrolledText

# pathdoctor = 'D:/Documents/ENSC/GitHub/AlBidert/docs/doctor.txt'
# pathdialogue = 'D:/Documents/ENSC/GitHub/AlBidert/docs/dials/'

# Creating tkinter GUI
class Interface(tk.Tk):
    def resultEmotion(self,vect):
        self.ecrire("Résultats de l'analyse : \n\n","Emotions");
        vectEmotion = ["       Colère","      Dégout","           Peur","Culpabilité","            Joie","   Tristesse","         Honte"];
        for i in range(len(vect)):
            self.ecrireEmotion(vectEmotion[i],vect[i]*100);
            
    def ecrireEmotion(self,emotion,pourcentage):
        pourcentage = np.around(pourcentage);
        self.ecrire(emotion+" : ","Emotions")
        # self.ChatBox.insert("end + 100 chars"," "*int(pourcentage),"Remplissage");
        self.ecrire(" "*int(pourcentage),"Remplissage");
        self.ecrire("  "+str(int(pourcentage))+'%\n\n',"User");
   
    def ecrire(self,msg,tag):
        self.ChatBox.insert(tk.END,msg,tag);
        
   
    def configurationTag(self):
        self.ChatBox.tag_configure("Info", foreground="black", font=("Verdana",11,"bold","italic"));
        self.ChatBox.tag_configure("User", foreground="black",font=("Verdana",11));
        self.ChatBox.tag_configure("AlBidert", foreground="#29947c", font=("Verdana",11,"bold"));
        self.ChatBox.tag_configure("Remplissage",background="#3c9d9b",foreground="#3c9d9b", font=("Verdana",13,"bold"));
        self.ChatBox.tag_configure("Emotions",foreground="black", font=("Arial",11,"bold"))
   
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)

        self.title("AlBidert")
        # self.geometry("400x500")
        self.geometry("815x650")

        self.chatbot = Eliza()
        self.chatbot.load(pathdoctor)
        self.initialize()

    def initialize(self):
        # Create Chat window
        self.ChatBox = tk.Text(self, bd=0, bg="white", height="8", width="50", foreground="#000000", font=("Verdana",11))

        #Configuration de tags pour la mise en forme
        self.configurationTag();
        
        #Phrases initiales
        self.ecrire("AlBidert est un chatbot à qui vous pouvez parler librement et qui analysera vos émotions.\nQuand vous avez terminé, entrez le mot-clé 'DONE'.\n\n","Info")
        self.ecrire("AlBidert: "+self.chatbot.initial()+"\n\n","AlBidert");
        # self.ChatBox.config(state=tk.DISABLED)

        # Bind scrollbar to Chat window
        self.scrollbar = tk.Scrollbar(self, command=self.ChatBox.yview, cursor="heart")
        self.ChatBox['yscrollcommand'] = self.scrollbar.set

        # Create the box to enter message
        self.EntryBox = tk.Text(self, bd=0, bg="white", height="8", width="50", foreground="#000000", font=("Verdana",11))
        self.EntryBox.focus()
        self.EntryBox.bind("<Return>", lambda event: self.get_response())

        # Create Button to send message
        self.SendButton = tk.Button(self, font=("Verdana", 12, 'bold'), text="Envoyer", width="10", height=5,
                            bd=0, bg="#3c9d9b", activebackground="#50e679", fg='#FFFFFF',activeforeground="#FFFFFF",
                            command=self.get_response)

        # Place all components on the screen
        self.scrollbar.place(x=796, y=6, height=530)
        self.ChatBox.place(x=6, y=6, height=530, width=790)
        self.EntryBox.place(x=6, y=551, height=90, width=670)
        self.SendButton.place(x=680, y=551, height=90)

    def get_response(self):
        currentFile=pathdialogue+"dialogue"+str(self.chatbot.num_fichier)+".txt"
        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", tk.END)

        #Analyse des émotions
        if msg != '':
            if msg == "done" or msg=="DONE":
                #Albidert dit aurevoir
                bye = self.chatbot.final()
                aurevoir = GoogleTranslator(target="fr").translate(bye)
                self.ecrire("AlBidert: " + aurevoir + '\n\n',"AlBidert")
                self.ecrire("Analyse de vos émotions en cours...\n\n","Info")
                self.ChatBox.yview(tk.END)
                #---Analyse de tout le texte d'un seul bloc---#
                #Recupérer le fichier texte sans la première ligne qui est vide#
                if (os.path.isfile(currentFile)):
                    with open(currentFile) as f:
                    # with open(pathdialogue+"dialogue.txt") as f :
                        texte_fr = f.read()
                        if (texte_fr !='') :
                            texte_en = GoogleTranslator().translate(texte_fr)

                            #Transformer ce fichier texte en vecteur#
                            vector = stringToVect(texte_en);

                            #utiliser le model pour predire#
                            model = joblib.load(pathModel)
                            prediction = model.predict_proba(vector.reshape(1,-1))[0];
                            
                            #Affichage résultats
                            self.resultEmotion(prediction)

                            self.ChatBox.config(state=tk.DISABLED)
                            self.ChatBox.yview(tk.END)
                else :
                    print("ERROR : Rien à analyser");
                    self.destroy();
            else :
                write_in_file(pathdialogue+"dialogue"+str(self.chatbot.num_fichier)+".txt",msg)
                self.ChatBox.config(state=tk.NORMAL)
                self.ChatBox.insert(tk.END, "You: " + msg + '\n\n',"User")
                self.ChatBox.yview(tk.END)
                # print(GoogleTranslator().translate(msg)); #anglais par défaut
                res = self.chatbot.respond(GoogleTranslator().translate(msg)); #anglais par défaut

                # if res == "quit":
                #     res = self.chatbot.final()
                
                rep = GoogleTranslator(target="fr").translate(res)
                self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n',"AlBidert")
                self.ChatBox.yview(tk.END)
