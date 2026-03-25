def est_standard(automate):
    """
    Vérifie si un automate est standart ou non
    :param automate: l'automate dont on veut verifier si il est standard
    :return: True ou false
    """
    if len(automate["initiaux"]) != 1:
        return False
    init = automate["initiaux"][0]
    for (tran) in automate["transitions"]:
        if tran[2] == init:
            return False
    return True


def standardiser(automate):
    """
    Standardise un automate
    :param automate: l'automate a standardiser
    :return: l'automate standardisé
    """
    if est_standard(automate):
        print("deja standardisé")
        return automate
    i = automate["nb_etats"]
    reconnait_mot_vide = False
    for e in automate["initiaux"]:
        if e in automate["finaux"]:
            reconnait_mot_vide = True

    if reconnait_mot_vide:
        automate["finaux"].append(i)

    for etat_initial in automate["initiaux"]:
        for (src, lettre, dst) in automate["transitions"]:
            if src == etat_initial:
                nouvelle = (i, lettre, dst)
                if nouvelle not in automate["transitions"]:
                    automate["transitions"].append(nouvelle)

    automate["initiaux"] = [i]
    automate["nb_etats"] += 1
    return automate