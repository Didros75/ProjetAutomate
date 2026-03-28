"""
Gère la création de 44 fichiers .txt dans un dossier traces
pour suivre la trace d'exécution des 44 automates
"""

import sys

import utile
from utile import txt_dictionnaire, afficher_automate
from standardisation import est_standard, standardiser
from determinisation_completion import *
from minimisation import minimise
import os

fichiers_automates = "automates"
os.mkdir("traces/")
dossier = "traces/"

def traiter_automate(numero):
    """
    redirige la sortie du terminal dans un fichier .txt
    pour ensuite réaliser une trace d'execution d'un automates donnée
    :param numero: numero coorespondant à l'automate à traiter
    :return: none
    """
    with open(f"{dossier}automate_{numero:02d}.txt", "w", encoding="utf-8") as f:
        sys.stdout = f

        print(f"AUTOMATE #{numero:02d}")

        #Lecture
        print("\n>>> LECTURE DE L'AUTOMATE\n")
        automate = txt_dictionnaire(fichiers_automates, f"{numero:02d}")
        utile.afficher_automate(automate)

        #Standardisation
        print("\n>>> STANDARDISATION\n")
        if est_standard(automate):
            print("Déjà standard.")
        else:
            print("Non standard -> standardisation...")
            automate = standardiser(automate)
            utile.afficher_automate(automate)

        #Déterminisation et complétion
        print("\n>>> DÉTERMINISATION ET COMPLÉTION\n")
        AFDC = determiniser_et_completer(automate)

        #Minimisation
        print("\n>>> MINIMISATION\n")
        AFDCM = minimise(AFDC)
        utile.afficher_automate(automate)

        print(f"\nFIN DU TRAITEMENT DE L'AUTOMATE #{numero:02d}")
        sys.stdout = sys.__stdout__

"""exécution du programme sur les 44 automates"""
if __name__ == "__main__":
    for n in range(1, 45):
        traiter_automate(n)