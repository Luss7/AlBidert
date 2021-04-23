import csv
from catalogue import check_exists
import spacy
import os
import pandas as pd

nlp = spacy.load('en_core_web_md');

fichier_in ="ISEAR_0/isear_databank/isear_clean.csv"
fichier_out="ISEAR_0/isear_vector/isear_vector.csv"
if os.path.exists(fichier_out):
    os.remove(fichier_out)

with open(fichier_in,"r")as file_in:
    with open(fichier_out, "w",newline="") as file_out:
        title="Emotion"
        for i in range(0,300):
            title=title+",Text_"+str(i);
        title=title+"\n";
        file_out.write(title);
        data = [];
        for line in file_in:
            if "Emotion,Text" not in line:
                emotion, text = line.split(",",1)
                vect=emotion.split()+nlp(text).vector.tolist();
                data.append(vect);
        writer = csv.writer(file_out)
        writer.writerows(data);     
    file_out.close;
file_in.close;
