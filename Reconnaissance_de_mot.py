import  determinisation_completion

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

    #determinisation_completion.determiniser_et_completer(auto)
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