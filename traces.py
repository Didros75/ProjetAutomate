import sys
from utile import txt_dictionnaire, afficher_automate
from standardisation import est_standard, standardiser
from determinisation_completion import *
from minimisation import minimise


fichiers_automates = "automates"
dossier = "traces/"

def traiter_automate(numero):
    with open(f"{dossier}automate_{numero:02d}.txt", "w", encoding="utf-8") as f:
        sys.stdout = f

        print(f"AUTOMATE #{numero:02d}")

        # 1. Lecture
        print("\n>>> LECTURE DE L'AUTOMATE\n")
        automate = txt_dictionnaire(fichiers_automates, f"{numero:02d}")
        afficher_automate(automate)

        # 2. Standardisation
        print("\n>>> STANDARDISATION\n")
        if est_standard(automate):
            print("Déjà standard.")
        else:
            print("Non standard -> standardisation...")
            automate = standardiser(automate)
            afficher_automate(automate)

        # 3. Déterminisation & complétion
        print("\n>>> DÉTERMINISATION ET COMPLÉTION\n")
        AFDC = determiniser_et_completer(automate)

        # 4. Minimisation
        print("\n>>> MINIMISATION\n")
        AFDCM = minimise(AFDC)
        afficher_automate(AFDCM)

        print(f"\nFIN DU TRAITEMENT DE L'AUTOMATE #{numero:02d}")
        sys.stdout = sys.__stdout__

# exécution du programme sur les 44 automates
for n in range(1, 45):
    traiter_automate(n)