from csvVect import csvTextToCsvVect, enleverGuillement
from fonctionML import exportMlpLearning

if __name__ == '__main__':
    fichier_in ="D:/Documents/ENSC/GitHub/AlBidert/docs/ISEAR_0/isear_databank/isear_clean.csv"
    fichier_in_clean = "D:/Documents/ENSC/GitHub/AlBidert/docs/ISEAR_0/isear_databank/isear_clean_clean.csv"
    fichier_out="D:/Documents/ENSC/GitHub/AlBidert/docs/ISEAR_0/isear_vector/isear_vector.csv"

    #Remplacer le texte de chaque ligne d'un fichier csv par son vecteur associé#
    print("Elèvement des guillets autour des phrases...")
    enleverGuillement(fichier_in,fichier_in_clean);
    print("Done")
    print("Remplacement du texte par vecteur...")
    csvTextToCsvVect(fichier_in_clean,fichier_out);
    print("Done")

    #Algo de Machine Learning 
    fichier_csv=fichier_out
    fichier_modele = "D:/Documents/ENSC/GitHub/AlBidert/docs/models/mlp_model5.pkl"
    print("Algo Machine Learning")
    exportMlpLearning(fichier_csv,fichier_modele)
    print("Done")

    