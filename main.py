"""
Gère la boucle principale, les menus, et l'enchaînement de toutes
les étapes de traitement d'un automate fini.
"""

import utile
import determinisation_completion
import standardisation
import Reconnaissance_de_mot
import langage_complementaire
import mermaid
import minimisation

#  Constantes ANSI pour la couleur dans le terminal

RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[96m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
GREY    = "\033[90m"

def titre(texte):
    """
    Affiche un titre encadré bien visible.
    :param texte: le texte du titre
    """
    largeur = 60
    print()
    print(CYAN + "╔" + "═" * largeur + "╗" + RESET)
    print(CYAN + "║" + RESET + BOLD + texte.center(largeur) + RESET + CYAN + "║" + RESET)
    print(CYAN + "╚" + "═" * largeur + "╝" + RESET)
    print()


def sous_titre(texte):
    """
    Affiche un sous-titre avec une ligne de séparation.
    :param texte: le texte du sous-titre
    """
    print()
    print(YELLOW + "  ┌─ " + BOLD + texte + RESET + YELLOW + " " + "─" * max(0, 54 - len(texte)) + "┐" + RESET)
    print()


def separateur():
    """Affiche une ligne de séparation légère."""
    print(GREY + "  " + "─" * 58 + RESET)


def succes(texte):
    """Affiche un message de succès."""
    print(GREEN + "  ✔  " + RESET + texte)


def erreur(texte):
    """Affiche un message d'erreur."""
    print(RED + "  ✖  " + RESET + texte)


def info(texte):
    """Affiche un message d'information."""
    print(BLUE + "  ℹ  " + RESET + texte)


def question(texte):
    """Pose une question à l'utilisateur et retourne sa réponse."""
    return input(MAGENTA + "  ?  " + RESET + texte + " → ")


def menu_choix(options):
    """
    Affiche un menu numéroté et retourne le numéro choisi.
    :param options: liste de chaînes de caractères décrivant chaque option
    :return: le numéro du choix (int) entre 1 et len(options)
    """
    for i, opt in enumerate(options, 1):
        print(f"  {CYAN}{i}{RESET}  {opt}")
    print()
    while True:
        choix = question(f"Votre choix (1–{len(options)})")
        if choix.isdigit() and 1 <= int(choix) <= len(options):
            return int(choix)
        erreur(f"Entrez un nombre entre 1 et {len(options)}.")


def attendre():
    """Pause : attend que l'utilisateur appuie sur Entrée."""
    print()
    input(GREY + "  [ Appuyez sur Entrée pour continuer... ]" + RESET)

#  Écran d'accueil méga stylé :)

def ecran_accueil():
    """Affiche écran de bienvenue au lancement."""
    print("\033[2J\033[H", end="")   # efface le terminal
    print()
    print(CYAN + r"""
   ███████╗███████╗██████╗ ███████╗██╗
   ██╔════╝██╔════╝██╔══██╗██╔════╝██║
   █████╗  █████╗  ██████╔╝█████╗  ██║
   ██╔══╝  ██╔══╝  ██╔══██╗██╔══╝  ██║
   ███████╗██║     ██║  ██║███████╗██║
   ╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝
    """ + RESET)
    print(BOLD + WHITE + "         Automates Finis & Expressions Rationnelles".center(62) + RESET)
    print(GREY   + "                              EFREI P2 — 2025/2026".center(62) + RESET)
    print(RED + "          Julie - Eliott - Melvin - Ethan - Arthur".center(62) + RESET)
    print()
    separateur()
    print()

#  Chargement d'un automate

def charger_automate():
    """
    Demande à l'utilisateur quel automate charger depuis le fichier 'automates'.
    Retourne le dictionnaire de l'automate, ou None en cas d'échec.
    :return: dictionnaire automate ou None
    """
    sous_titre("Chargement de l'automate")
    info("Les automates disponibles sont numérotés de 01 à 44.")
    numero = question("Numéro de l'automate à charger (ex: 8 ou 08)")

    # On accepte '8' ou '08'
    numero = numero.strip().zfill(2)

    auto = utile.txt_dictionnaire("automates", numero)
    if auto is None:
        erreur(f"Automate #{numero} introuvable dans le fichier 'automates'.")
        return None

    succes(f"Automate #{numero} chargé avec succès.")
    return auto, numero

#  Étape 1 — Affichage + informations

def etape_affichage(auto, numero):
    """
    Affiche l'automate et indique s'il est déterministe, standard, complet.
    :param auto: dictionnaire de l'automate
    :param numero: numéro de l'automate (str)
    """
    sous_titre(f"Automate #{numero} — Affichage")
    utile.afficher_automate(auto)

    separateur()
    sous_titre("Propriétés de l'automate")

    # on regarde s'il est standard
    est_std = standardisation.est_standard(auto)
    if est_std:
        succes("L'automate est STANDARD.")
    else:
        erreur("L'automate n'est PAS standard.")

    # on regarde s'il est déterministe
    # On affiche le résultat ; la fonction affiche déjà les raisons si non-det.
    est_det = determinisation_completion.est_deterministe(auto)
    if est_det:
        succes("L'automate est DÉTERMINISTE.")
    else:
        erreur("L'automate n'est PAS déterministe (raisons affichées ci-dessus).")

    # On regarde s'il est complet
    if est_det:
        est_cpl = determinisation_completion.est_complet(auto)
        if est_cpl:
            succes("L'automate est COMPLET.")
        else:
            erreur("L'automate n'est PAS complet (raisons affichées ci-dessus).")
    else:
        info("Vérification de la complétude ignorée (automate non déterministe).")

    return est_std, est_det

#  Étape 2 — Standardisation (si besoin)

def etape_standardisation(auto):
    """
    Propose à l'utilisateur de standardiser l'automate s'il ne l'est pas.
    :param auto: dictionnaire de l'automate
    :return: l'automate (éventuellement standardisé)
    """
    sous_titre("Standardisation")

    if standardisation.est_standard(auto):
        info("L'automate est déjà standard — aucune action nécessaire.")
        return auto

    choix = question("Voulez-vous standardiser l'automate ? (o/n)")
    if choix.lower() in ("o", "oui", "y", "yes"):
        auto = standardisation.standardiser(auto)
        succes("Automate standardisé.")
        separateur()
        sous_titre("Automate standardisé")
        utile.afficher_automate(auto)
    else:
        info("Standardisation ignorée à la demande de l'utilisateur.")

    return auto

#  Étape 3 — Déterminisation & complétion

def etape_determinisation(auto):
    """
    Déterminise et complète l'automate selon le pseudo-code du sujet.
    :param auto: dictionnaire de l'automate
    :return: l'automate déterministe et complet (AFDC)
    """
    sous_titre("Déterminisation & Complétion")

    AFDC = determinisation_completion.determiniser_et_completer(auto)

    separateur()
    sous_titre("Automate Déterministe et Complet (AFDC)")
    utile.afficher_automate(AFDC)

    return AFDC

#  Étape 4 — Minimisation


def etape_minimisation(AFDC):
    """
    Minimise l'automate déterministe complet.
    :param AFDC: dictionnaire de l'automate déterministe et complet
    :return: l'automate minimal (AFDCM)
    """
    sous_titre("Minimisation")
    info("Calcul de l'automate minimal en cours...")

    AFDCM = minimisation.minimise(AFDC)

    separateur()
    sous_titre("Automate Minimal (AFDCM)")
    utile.afficher_automate(AFDCM)

    return AFDCM

#  Étape 5 — Reconnaissance de mots

def etape_reconnaissance(AFDC):
    """
    Lance la boucle de reconnaissance de mots sur l'AFDC.
    :param AFDC: dictionnaire de l'automate déterministe et complet
    """
    sous_titre("Reconnaissance de mots")
    info("Tapez un mot pour tester s'il appartient au langage reconnu.")
    info("Tapez  'fin'  pour arrêter la reconnaissance.")
    print()

    Reconnaissance_de_mot.reconnaissance(AFDC)

    succes("Fin de la reconnaissance de mots.")

#  Étape 6 — Langage complémentaire

def etape_complementaire(AFDC, AFDCM):
    """
    Construit et affiche l'automate reconnaissant le langage complémentaire.
    :param AFDC:  automate déterministe et complet
    :param AFDCM: automate minimal
    """
    sous_titre("Langage Complémentaire")

    print("  Sur quel automate calculer le complémentaire ?")
    print()
    choix = menu_choix([
        "L'AFDC  (Automate Déterministe et Complet)",
        "L'AFDCM (Automate Minimal)",
    ])

    if choix == 1:
        base = AFDC
        info("Complémentaire calculé à partir de l'AFDC.")
    else:
        base = AFDCM
        info("Complémentaire calculé à partir de l'AFDCM.")

    # La fonction complementation gère l'affichage
    AComp = langage_complementaire.complementation(base)

    separateur()
    sous_titre("Automate Complémentaire (AComp)")
    utile.afficher_automate(AComp)

    return AComp

#  Menu de traitement d'un automate

def traiter_automate():
    """
    Gère l'ensemble du cycle de traitement d'un automate :
    chargement -> affichage -> standardisation -> déterminisation
    -> minimisation -> reconnaissance -> complémentaire.
    L'utilisateur peut choisir les étapes à effectuer via un menu.
    """

    # Chargement
    resultat = charger_automate()
    if resultat is None:
        attendre()
        return
    auto, numero = resultat
    attendre()

    # Variables qui seront remplies au fil des étapes
    AFDC  = None
    AFDCM = None

    # Boucle du menu de traitement
    while True:
        titre(f"Automate #{numero} — Menu de traitement")

        # Affichage dynamique selon l'état d'avancement
        etapes = [
            f"{'[✔] ' if True else ''}  Afficher l'automate & ses propriétés",
            f"Standardiser l'automate",
            f"{'[✔] ' if AFDC  else ''}  Déterminiser & compléter  {'→ AFDC disponible' if AFDC  else ''}",
            f"{'[✔] ' if AFDCM else ''}  Minimiser                  {'→ AFDCM disponible' if AFDCM else '(AFDC requis)'}",
            f"Reconnaître des mots       {'(AFDC requis)' if not AFDC else ''}",
            f"Construire le langage complémentaire  {'(AFDC requis)' if not AFDC else ''}",
            f"Changer d'automate (retour au chargement)",
            f"Convertir en Mermaid (Bonus)",
            f"Quitter le programme",
        ]
        choix = menu_choix(etapes)

        print("\033[2J\033[H", end="")   # efface le terminal

        # 1. Affichage
        if choix == 1:
            etape_affichage(auto, numero)
            attendre()

        # 2. Standardisation
        elif choix == 2:
            auto = etape_standardisation(auto)
            # Si on re-standardise, AFDC et AFDCM ne sont plus valides
            AFDC  = None
            AFDCM = None
            attendre()

        # 3. Déterminisation
        elif choix == 3:
            AFDC  = etape_determinisation(auto)
            AFDCM = None   # la minimisation doit être refaite
            attendre()

        # 4. Minimisation
        elif choix == 4:
            if AFDC is None:
                erreur("Vous devez d'abord déterminiser & compléter l'automate (étape 3).")
            else:
                AFDCM = etape_minimisation(AFDC)
            attendre()

        # 5. Reconnaissance de mots
        elif choix == 5:
            if AFDC is None:
                erreur("Vous devez d'abord déterminiser & compléter l'automate (étape 3).")
                attendre()
            else:
                etape_reconnaissance(AFDC)
                attendre()

        # 6. Langage complémentaire
        elif choix == 6:
            if AFDC is None:
                erreur("Vous devez d'abord déterminiser & compléter l'automate (étape 3).")
                attendre()
            else:
                # Si AFDCM n'est pas calculé, on ne propose que l'AFDC
                if AFDCM is None:
                    info("L'AFDCM n'est pas encore calculé : seul l'AFDC sera proposé.")
                    sous_titre("Langage Complémentaire")
                    info("Complémentaire calculé à partir de l'AFDC.")
                    AComp = langage_complementaire.complementation(AFDC)
                    separateur()
                    sous_titre("Automate Complémentaire (AComp)")
                    utile.afficher_automate(AComp)
                else:
                    etape_complementaire(AFDC, AFDCM)
                attendre()

        # 7. Changer d'automate
        elif choix == 7:
            print("\033[2J\033[H", end="")
            return   # retour à la boucle principale -> chargement d'un autre automate

        # 8. Chargement en Mermaid
        elif choix == 8:

            print()
            print("Choisissez la forme que vous souhaitez exporter : ")
            liste = [f"Automate de base", f"Automate determinisé", f"Automate minimisé"]
            nouveau_choix=menu_choix(liste)
            if nouveau_choix == 1:
                auto2=auto
            elif nouveau_choix == 2:
                auto2=determinisation_completion.determiniser_et_completer(auto)
            elif nouveau_choix == 3:
                auto3=determinisation_completion.determiniser_et_completer(auto)
                auto2=minimisation.minimise(auto3)
            print()
            choix_fichier = input("Choisissez le nom du fichier : ")
            mermaid.exporter_mermaid(auto2, choix_fichier)
            attendre()


        # 9. Quitter
        elif choix == 9:
            titre("Au revoir !")
            print(GREY + "  Merci d'avoir utilisé ce programme." + RESET)
            print()
            exit(0)

#  Boucle principale

def main():
    """
    Point d'entrée du programme.
    Affiche l'écran d'accueil puis lance la boucle principale
    permettant de traiter plusieurs automates sans relancer le programme.
    """
    ecran_accueil()

    titre("Bienvenue")
    info("Ce programme vous permet de travailler sur des automates finis.")
    info("Vous pouvez traiter autant d'automates que vous le souhaitez.")
    info("Tous les automates de test sont stockés dans le fichier 'automates'.")
    print()
    attendre()

    # Boucle principale : traitement de plusieurs automates
    while True:
        print("\033[2J\033[H", end="")
        titre("Chargement d'un automate")
        traiter_automate()

#  Lancement

if __name__ == "__main__":
    main()
