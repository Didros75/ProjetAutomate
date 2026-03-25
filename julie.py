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

    # Affichage de l'alphabet

    str_alphabet = "\t|\t"
    for elem in alphabet :
        str_alphabet += elem + "\t|\t"
    print(str_alphabet)
    print("---------------------")

    # Affichage des transitions

    for i in range(etats) :
        str_ligne = str(i) + "\t|\t"
        for lettre in alphabet :
            for elem in dict_transi[i][lettre] :
                str_ligne += str(elem) + " "
            str_ligne += "\t|\t"

        # Ecriture si c'est un état final ou initial

        if i in initiaux :
            str_ligne += "\tEtat initial"
        if i in finaux :
            str_ligne += "\tEtat final"

        print(str_ligne)

# Reconnaissance de mots

def lire_mot(mot) :
    """
    Demande un mot à vérifier à l'utilisateur
    :param mot: le mot, une chaine de caractère
    :return: le mot
    """
    print("Ecrire un mot à vérifier (écrire fin pour stopper la vérification) :")
    mot = ""
    return input(mot)

def reconnaitre_mot(mot, auto) :
    """
    Vérifie si le mot donné en paramètre est reconnu par l'automate ou non
    :param mot: le mot à vérifier, chaine de caractère
    :param A: un dictionnaire rprésentant l'automate
    :return: oui si le mot est reconnu, non sinon
    """

    # ATTENTION : Utiliser la fonction de Melvin pour déterminiser

    etat_actuel = auto["initiaux"][0]

    while mot != "":
        transition_trouvee = False

        for elem in auto['transitions']:
            if etat_actuel == elem[0] and mot[0] == elem[1]:
                etat_actuel = elem[2]
                mot = mot[1:]
                transition_trouvee = True
                break

        if not transition_trouvee:
            return "non"

    if etat_actuel in auto["finaux"]:
        return "oui"
    return "non"

def reconnaissance(auto) :
    """
    lance la reconnaissance des mots jusq'au mot "fin"
    :return: none
    """
    mot = ""
    while mot != "fin" :
        mot = lire_mot(mot)
        reponse = reconnaitre_mot(mot, auto)
        print(reponse)

# Langage complémentaire

def complementation(auto) :
    """
    Appelle la fonction qui complémente l'automate
    :param auto: le dictionnaire de l'automate initial
    :return: le dictionnaire de l'automate complémentaire
    """
    AComp = automate_complementaire(auto)
    afficher_automate(AComp)
    return AComp

def automate_complementaire(auto) :
    """
    Créer l'automate qui reconnaît le langage complémentaire
    :param auto: le dictionnaire de l'automate initial
    :return: le dictionnaire de l'automate complémentaire
    """

    nv_finaux = [i for i in range(auto["nb_etats"])]
    for elem in auto["finaux"] :
        nv_finaux.remove(elem)

    auto["finaux"] = nv_finaux
    return auto

complementation({'nb_etats': 5, 'alphabet': ['a', 'b'], 'initiaux': [1, 3], 'finaux': [2, 4], 'transitions': [(1, 'a', 2), (1, 'b', 0), (3, 'a', 0), (3, 'b', 4), (0, 'a', 0), (0, 'b', 0)]})