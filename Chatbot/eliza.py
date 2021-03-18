import logging
import random
import re
from collections import namedtuple
from google_trans_new import google_translator
import fnmatch
import os, os.path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as ScrolledText

rnd = random.Random()
translator = google_translator()

# Fix Python2/Python3 incompatibility
try: input = raw_input
except NameError: pass

log = logging.getLogger(__name__)


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps


class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0


class Eliza:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

        dirpath = "D:/Documents/ENSC/GitHub/AlBidert/Eliza"
        self.num_fichier = len(fnmatch.filter(os.listdir(dirpath), "dialogue*.txt"))

    def load(self, path):
        key = None
        decomp = None
        with open(path,encoding='utf-8') as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)

    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                log.debug('Decomp did not match: %s', decomp.parts)
                continue
            log.debug('Decomp matched: %s', decomp.parts)
            log.debug('Decomp results: %s', results)
            results = [self._sub(words, self.posts) for words in results]
            log.debug('Decomp results after posts: %s', results)
            reasmb = self._next_reasmb(decomp)
            log.debug('Using reassembly: %s', reasmb)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                log.debug('Goto key: %s', goto_key)
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                log.debug('Saved to memory: %s', output)
                continue
            return output
        return None

    def respond(self, text):
        for words in text.split(' '):
            if words in self.quits:
                return "quit"
        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)
        log.debug('After punctuation cleanup: %s', text)

        words = [w for w in text.split(' ') if w]
        log.debug('Input: %s', words)

        words = self._sub(words, self.pres)
        log.debug('After pre-substitution: %s', words)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)
        log.debug('Sorted keys: %s', [(k.word, k.weight) for k in keys])

        output = None

        for key in keys:
            output = self._match_key(words, key)
            if output:
                log.debug('Output from key: %s', output)
                break
        if not output:
            if self.memory:
                output =  rnd.choice(self.memory)
                log.debug('Output from memory: %s', output)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])
                log.debug('Output from xnone: %s', output)

        return " ".join(output)

    def initial(self):
        return rnd.choice(self.initials)

    def final(self):
        return rnd.choice(self.finals)

    def run(self):
        dirpath = "D:/Documents/ENSC/GitHub/AlBidert/Eliza"
        print(self.initial())
        nb_fichier_text = len(fnmatch.filter(os.listdir(dirpath), "dialogue*.txt"))
        
        while True:
            sent = input('> ')
            write_in_file("Eliza/dialogue"+str(nb_fichier_text+1)+".txt",sent)
            output = translator.translate(translator.translate(self.respond(sent),lang_tgt='en'),lang_tgt='fr')
            if output is None:
                break

            print(output)

        print(self.final())
    

# Creating tkinter GUI

class Interface(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)

        self.title("Chatbot")
        self.geometry("400x500")

        self.chatbot = Eliza()
        self.chatbot.load('D:/Documents/ENSC/GitHub/AlBidert/Eliza/doctor.txt')
        
        self.initialize()

    def initialize(self):
          
        # Create Chat window
        
        self.ChatBox = tk.Text(self, bd=0, bg="white", height="8", width="50", font="Arial",)
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

        write_in_file("Eliza/dialogue"+str(self.chatbot.num_fichier)+".txt","> "+msg)

        if msg != '':
            self.ChatBox.config(state=tk.NORMAL)
            self.ChatBox.insert(tk.END, "You: " + msg + '\n\n')
            self.ChatBox.config(foreground="#446665", font=("Verdana", 12))
            res = self.chatbot.respond(translator.translate(msg))

            if res == "quit":
                res = self.chatbot.final()

            rep = translator.translate(res,lang_tgt='fr')
            self.ChatBox.insert(tk.END, "AlBidert: " + rep + '\n\n')

            self.ChatBox.config(state=tk.DISABLED)
            self.ChatBox.yview(tk.END)


def main():
    eliza = Eliza()
    eliza.load('D:/Documents/ENSC/GitHub/AlBidert/Eliza/doctor.txt')
    eliza.run()
    
def write_in_file(path,texte):
    # ouverture du fichier_in en écriture
    with open(path, 'a', encoding='utf-8') as file_in:
        file_in.write('\n'+texte)

if __name__ == '__main__':
    logging.basicConfig()
    # main()
    interface = Interface()
    interface.mainloop() 
