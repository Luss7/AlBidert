import re
from catalogue import check_exists
import spacy
import os

nlp = spacy.load('en_core_web_md');

fichier_in ="ISEAR_0/isear_databank/isear_clean.csv"
fichier_out="ISEAR_0/isear_vector/isear_vector.csv"
if os.path.exists(fichier_out):
    os.remove(fichier_out)

with open(fichier_in,"r")as file_in:
    with open(fichier_out, 'a',encoding='utf-8') as file_out:
        file_out.write("Text\n");
        for line in file_in:
            if "Emotion,Text" not in line:
                emotion, text = line.split(",",1)
                vect=str(nlp(text).vector.tolist());
                file_out.write(str(vect)+"\n");

