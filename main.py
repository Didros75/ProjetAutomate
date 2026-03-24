def txt_dictionnaire(fichier, numero):
    """
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
                t = lignes[i]
                etat_dep = int(t[0])
                symbole = t[1]
                etat_arr = int(t[2])
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



def est_standard(automate):
    """
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



auto = txt_dictionnaire("automates", "05")
print(auto)
auto2 = standardiser(auto)
print(auto2)
