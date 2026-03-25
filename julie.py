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
    print("\tQ = ", sorted(liste_etats))

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

    afficher_transitions(auto)

def afficher_transitions(auto):
    etats = auto['nb_etats']
    alphabet = auto['alphabet']
    transitions = auto['transitions']
    initiaux = auto['initiaux']
    finaux = auto['finaux']

    # Définition d'un dictionnaire pour stocker les transitions

    dict_transi = {}
    for i in range(etats) :
        dict_transi[i] = {}
        for elem in alphabet :
            dict_transi[i][elem] = []

    for elem in transitions :
        dict_transi[elem[0]][elem[1]].append(elem[2])

    str_alphabet = "\t|\t"
    for elem in alphabet :
        str_alphabet += elem + "\t|\t"
    print(str_alphabet)
    print("---------------------")

    for i in range(etats) :
        str_ligne = str(i) + "\t|\t"
        for lettre in alphabet :
            for elem in dict_transi[i][lettre] :
                str_ligne += str(elem) + " "
            str_ligne += "\t|\t"
        print(str_ligne)

afficher_automate({'nb_etats': 5, 'alphabet': ['a', 'b'], 'initiaux': [1, 3], 'finaux': [2, 4], 'transitions': [(1, 'a', 2), (1, 'b', 0), (3, 'a', 0), (3, 'b', 4), (0, 'a', 0), (0, 'b', 0)]})

# Reconnaissance de mots

def lire_mot(mot) :
    """

    :param mot:
    :return:
    """

def reconnaitre_mot() :
    pass

def reconnaissance() :
    """

    :return: none
    """
    pass