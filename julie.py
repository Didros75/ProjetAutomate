import  determinisation_completion

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

    afficher_transitions(auto, liste_etats)

def afficher_transitions(auto, liste_etats):
    etats = auto['nb_etats']
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
    print("------" * 3 + "-" * 3 * (taille_max))

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

    determinisation_completion.determiniser_et_completer(auto)
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

    determinisation_completion.determiniser_et_completer(auto)

    nv_finaux = [i for i in range(auto["nb_etats"])]
    for elem in auto["finaux"] :
        nv_finaux.remove(elem)

    auto["finaux"] = nv_finaux
    return auto

afficher_automate({'nb_etats': 5, 'alphabet': ['a', 'b'], 'initiaux': [1, 3], 'finaux': [2, 4], 'transitions': [(1, 'a', 2), (1, 'b', 0), (3, 'a', 0), (3, 'b', 4), (0, 'a', 0), (0, 'b', 0)]})