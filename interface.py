#! /Program/Python/python37
# coding: utf-8
# interface.py

from eliza import Eliza
from eliza import write_in_file
from eliza import translator
from eliza import pathdoctor
from eliza import pathdialogue
import tkinter as tk
# import tkinter.ttk as ttk
# import tkinter.scrolledtext as ScrolledText

# pathdoctor = 'D:/Documents/ENSC/GitHub/AlBidert/docs/doctor.txt'
# pathdialogue = 'D:/Documents/ENSC/GitHub/AlBidert/docs/dials/'

# Creating tkinter GUI
class Interface(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)

        self.title("Chatbot")
        self.geometry("400x500")

        self.chatbot = Eliza()
        self.chatbot.load(pathdoctor)
        
        self.initialize()

    def initialize(self):
          
        # Create Chat window
        
        self.ChatBox = tk.Text(self, bd=0, bg="white", height="8", width="50", font="Arial",)
        self.ChatBox.insert(tk.END,"*AlBidert est un chatbot à qui vous pouvez parler librement et qui analysera vos émotions. Pour cela, entrez le mot-clé 'done'.*\n\n");
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
                            bd=0, bg="#f9a602", activebackground="#3c9d9b", fg='#000000',
                            command=self.get_response())

        # Place all components on the screen
        self.scrollbar.place(x=376, y=6, height=386)
        self.ChatBox.place(x=6, y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)

    def get_response(self):

        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", tk.END)

        if msg != '':
            if msg == "done":
                #Affichage de la réponse de l'utilisateur
                self.ChatBox.config(state=tk.NORMAL)
                self.ChatBox.config(foreground="#446665", font=("Verdana", 12))
                #Albidert dit aurevoir
                res = self.chatbot.final()
                rep = translator.translate(res,lang_tgt='fr')
                self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n')

                self.ChatBox.insert(tk.END,"*Analyse de vos émotions en cours...*\n\n");
                self.ChatBox.config(state=tk.DISABLED)
                self.ChatBox.yview(tk.END)
            else :
                write_in_file(pathdialogue+"dialogue"+str(self.chatbot.num_fichier)+".txt",msg)
                self.ChatBox.config(state=tk.NORMAL)
                self.ChatBox.insert(tk.END, "You: " + msg + '\n\n')
                self.ChatBox.config(foreground="#446665", font=("Verdana", 12))
                print(translator.translate(msg)); #anglais par défaut
                res = self.chatbot.respond(translator.translate(msg))

                # if res == "quit":
                #     res = self.chatbot.final()
                
                rep = translator.translate(res,lang_tgt='fr')
                self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n')
                self.ChatBox.config(state=tk.DISABLED)
                self.ChatBox.yview(tk.END)