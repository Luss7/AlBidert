import csv
import spacy
import os

# fichier_in ="docs/ISEAR_0/isear_databank/isear_clean.csv"
# fichier_out="docs/ISEAR_0/isear_vector/isear_vector.csv"

def enleverGuillement(fichier_in,fichier_out):
    with open(fichier_in,"r") as file_in:
        with open(fichier_out,"w",encoding="utf-8") as file_out:
            for line in file_in:
                # print("line : ",line);
                emotion,text=line.split(",",1)
                if text[0]=="\"":
                    text=text[1:-2]+"\n"
                    # print("Nouveau text : ",text)
                file_out.write(emotion+","+text);

def csvTextToCsvVect(fichier_in,fichier_out):
    nlp = spacy.load('en_core_web_md');
    if os.path.exists(fichier_out):
        os.remove(fichier_out)
    print("Ouverture du fichier_in...");
    with open(fichier_in,"r")as file_in:
        with open(fichier_out, "w",newline="") as file_out:
            title="Emotion"
            for i in range(0,300):
                title=title+",Text_"+str(i);
            title=title+"\n";
            print("Ecriture 1ere ligne du fichier...");
            file_out.write(title);
            data = [];
            print("Traduction de chaque ligne en vecteur...");
            for line in file_in:
                if "Emotion,Text" not in line:
                    emotion, text = line.split(",",1)
                    vect=emotion.split()+nlp(text).vector.tolist();
                    data.append(vect);
            print("Ecriture dans le nouveau fichier...");
            writer = csv.writer(file_out)
            writer.writerows(data);
            print("Fermeture des fichiers...");     
        file_out.close;
    file_in.close;

