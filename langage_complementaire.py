import utile, determinisation_completion

def complementation(auto) :
    """
    Appelle la fonction qui complémente l'automate
    :param auto: le dictionnaire de l'automate initial
    :return: le dictionnaire de l'automate complémentaire
    """
    AComp = automate_complementaire(auto)
    utile.afficher_automate(AComp)
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