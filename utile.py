def txt_dictionnaire(fichier, numero):
    """
    Transforme un fichier en automate lisible par python
    :param fichier: prend en parametre un fichier (automates.txt) contenant les 44 automates
    :param numero: le numero de l'automate qu'on veut
    :return: un dictionnaire avec tous les parametres de l'automate : son nb d'etats, l'alphabet utilisé, les etats initiaux et finaux et une liste des transitions sous forme de tuple (ex: (1, 'b', 2), lien entre sommet 1 et 2 avec l'etat b)
    """
    with open(fichier, "r") as f:
        lignes = [l.strip() for l in f if l.strip() != ""]

    i = 0
    while i < len(lignes):
        if lignes[i] == f"#{numero}":
            i += 1

            # Taille alphabet
            taille_alphabet = int(lignes[i])
            alphabet = [chr(ord('a') + j) for j in range(taille_alphabet)]
            i += 1

            # Nombre d'états
            nb_etats = int(lignes[i])
            i += 1

            # États initiaux
            parts = list(map(int, lignes[i].split()))
            nb_initiaux = parts[0]
            initiaux = parts[1:]
            i += 1

            # États finaux
            parts = list(map(int, lignes[i].split()))
            nb_finaux = parts[0]
            finaux = parts[1:]
            i += 1

            # Nombre de transitions
            nb_transitions = int(lignes[i])
            i += 1

            transitions = []

            for _ in range(nb_transitions):
                t = lignes[i].strip()
                j = 0
                while j < len(t) and t[j].isdigit():
                    j += 1
                etat_dep = int(t[:j])
                k = j + 1
                while k < len(t) and not t[k].isdigit():
                    k += 1
                symbole = t[j:k]
                if symbole=="e" and "e" not in alphabet:
                    alphabet.append("e")
                etat_arr = int(t[k:])
                transitions.append((etat_dep, symbole, etat_arr))
                i += 1

            return {
                "nb_etats": nb_etats,
                "alphabet": alphabet,
                "initiaux": initiaux,
                "finaux": finaux,
                "transitions": transitions
            }

        else:
            i += 1

    return None

def afficher_automate(auto) :
    """
    Affiche (print) un automate
    :param auto: un dictionnaire représentant un automate
    :return: none
    """

    # Affichage de l'alphabet

    nb_symboles = len(auto["alphabet"])
    print(str(nb_symboles), "symboles dans l’alphabet :")
    print("\tA = ", auto["alphabet"])

    # Affichage des états existants

    liste_etats = []
    for elem in auto["transitions"] :
        if elem[0] not in liste_etats :
            liste_etats.append(elem[0])
        if elem[2] not in liste_etats :
            liste_etats.append(elem[2])
    print(str(auto["nb_etats"]), "états :")
    print("\tQ = ", liste_etats)

    # Affichage des états initiaux

    nb_initial = len(auto["initiaux"])
    print(str(nb_initial), "états initiaux :")
    print("\tI = ", sorted(auto["initiaux"]))

    # Affichage des états terminaux

    nb_terminal = len(auto["finaux"])
    print(str(nb_terminal), "états finaux :")
    print("\tT = ", sorted(auto["finaux"]))

    # Affichage du nombre de transitions

    nb_transitions = len(auto["transitions"])
    print(str(nb_transitions), "transitions")

    afficher_transitions(auto, liste_etats)

def afficher_transitions(auto, liste_etats):
    """
    Affiche la table de transition
    :param auto: le dictionnaire de l'automate
    :param liste_etats: la liste des états du graphe
    :return:
    """
    alphabet = auto['alphabet']
    transitions = auto['transitions']
    initiaux = auto['initiaux']
    finaux = auto['finaux']

    # Définition d'un dictionnaire pour stocker les transitions

    dict_transi = {}
    for elem in liste_etats :
        dict_transi[elem] = {}
        for lettre in alphabet :
            dict_transi[elem][lettre] = []

    for elem in transitions :
        dict_transi[elem[0]][elem[1]].append(elem[2])

    # Regarder quelle transition est la plus longue pour ajuster la table

    taille_max = 0
    for cle in dict_transi.keys():
        if len(str(cle)) > taille_max:
            taille_max = len(str(cle))

    # Affichage de l'alphabet

    str_alphabet = " " * (taille_max)+ "\t|\t"
    for elem in alphabet :
        str_alphabet += elem + " " * (taille_max-len(str(elem))) + "\t|\t"
    print(str_alphabet)
    print("   " + "------" * (len(alphabet)+1) + "-" * 3 * (taille_max))

    # Affichage des transitions

    for etat in liste_etats :
        str_ligne = str(etat) + " " * (taille_max-len(str(etat))) + "\t|\t"
        for lettre in alphabet :
            for elem in dict_transi[etat][lettre] :
                str_ligne += str(elem)
            str_ligne += " " * (taille_max-len(str(elem))) + "\t|\t"

        # Ecriture si c'est un état final ou initial

        if etat in initiaux :
            str_ligne += "\tEtat initial"
        if etat in finaux :
            str_ligne += "\tEtat final"

        print(str_ligne)