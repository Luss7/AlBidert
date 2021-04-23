#! /Program/Python/python37
# coding: utf-8
# interface.py

from deep_translator import GoogleTranslator
from eliza import Eliza
from eliza import write_in_file
from eliza import pathdoctor
from eliza import pathdialogue
import tkinter as tk
import joblib
import spacy
import numpy as np

pathModel='D:/Documents/ENSC/GitHub/AlBidert/docs/mlp_model.pkl'

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
    def style(self):
        self.ChatBox.config(foreground="#446665", font=("Verdana", 12))
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)

        self.title("AlBidert")
        # self.geometry("400x500")
        self.geometry("800x650")

        self.chatbot = Eliza()
        self.chatbot.load(pathdoctor)
        
        self.initialize()

    def initialize(self):
        # Create Chat window
        self.ChatBox = tk.Text(self, bd=0, bg="white", height="8", width="50", foreground="#000000", font=("Verdana",11))
        self.ChatBox.insert(tk.END,"*AlBidert est un chatbot à qui vous pouvez parler librement et qui analysera vos émotions.\n");
        self.ChatBox.insert(tk.END,"Pour cela, entrez le mot-clé 'done'.*\n\n");
        self.ChatBox.insert(tk.END,"AlBidert: "+self.chatbot.initial()+'\n\n');
        self.ChatBox.config(state=tk.DISABLED)

        # Bind scrollbar to Chat window
        self.scrollbar = tk.Scrollbar(self, command=self.ChatBox.yview, cursor="heart")
        self.ChatBox['yscrollcommand'] = self.scrollbar.set

        # Create the box to enter message
        self.EntryBox = tk.Text(self, bd=0, bg="white", width="29", height="5", font="Arial")
        self.EntryBox.focus()
        self.EntryBox.bind("<Return>", lambda event: self.get_response())


        # Create Button to send message
        self.SendButton = tk.Button(self, font=("Verdana", 12, 'bold'), text="Envoyer", width="10", height=5,
                            bd=0, bg="#3c9d9b", activebackground="#50e679", fg='#FFFFFF',activeforeground="#FFFFFF",
                            command=self.get_response)

        # Place all components on the screen
        self.scrollbar.place(x=776, y=6, height=786)
        self.ChatBox.place(x=6, y=6, height=530, width=770)
        self.EntryBox.place(x=128, y=551, height=90, width=665)
        self.SendButton.place(x=6, y=551, height=90)

    def get_response(self):
        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", tk.END)

        if msg != '':
            if msg == "done":
                #Affichage de la réponse de l'utilisateur
                # self.ChatBox.config(state=tk.NORMAL)
                # self.ChatBox.config(foreground="#446665", font=("Verdana", 12))
                #Albidert dit aurevoir
                res = self.chatbot.final()
                rep = GoogleTranslator(target="fr").translate(res)
                self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n')
                self.ChatBox.insert(tk.END,"*Analyse de vos émotions en cours...*\n\n");
                self.ChatBox.yview(tk.END)
                #---Analyse de tout le texte d'un seul bloc#
                #Recupérer le fichier texte sans la première ligne qui est vide#
                f=open(pathdialogue+"dialogue"+str(self.chatbot.num_fichier)+".txt")
                texte = GoogleTranslator().translate(f.read());
                print(GoogleTranslator().translate(texte));
                #print(texte);
                #Transformer ce fichier texte en vecteur#
                vector = stringToVect(texte);
                #print(vector);
                #utiliser le model pour predire#
                #-- Analyse phrase par phrase : texte = f.readlines()[1:];
                model = joblib.load(pathModel)
                prediction = model.predict_proba(vector.reshape(1,-1));
                predictionArrondi = np.around(prediction,decimals=2)
                self.ChatBox.insert(tk.END,"Colère, Dégout, Peur, Culpabilité, Joie, Tristesse, Honte")
                self.ChatBox.insert(tk.END,predictionArrondi)
                self.ChatBox.config(state=tk.DISABLED)
                self.ChatBox.yview(tk.END)
            else :
                write_in_file(pathdialogue+"dialogue"+str(self.chatbot.num_fichier)+".txt",msg)
                self.ChatBox.config(state=tk.NORMAL)
                self.ChatBox.insert(tk.END, "You: " + msg + '\n\n')
                print(GoogleTranslator().translate(msg)); #anglais par défaut
                res = self.chatbot.respond(GoogleTranslator().translate(msg)); #anglais par défaut

                # if res == "quit":
                #     res = self.chatbot.final()
                
                rep = GoogleTranslator(target="fr").translate(res)
                self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n')
                self.ChatBox.yview(tk.END)