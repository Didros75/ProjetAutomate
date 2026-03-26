def est_synchrone(automate):
    """
    :param automate: un automate pour verifier si il est synchrone
    :return: si l'automate est synchrone (si il n'a pas de e dans ses transitions)
    """
    for lettre in automate["alphabet"]:
        if lettre == "e":
            return False
    return True

def est_deterministe(automate):
    """
    :param automate: un automate pour verifier si il est deterministe
    :return: True si il est deterministe (si il a une seule entrée et si une lettre ne peux realiser qu'une seule transition)
    """
    if len(automate["initiaux"]) > 1:
        print(f"Non déterministe : plusieurs états initiaux {automate['initiaux']}")
        return False

    deterministe = True
    for lettre in automate["alphabet"]:
        for etat in range(automate["nb_etats"]):
            cibles = [dst for (src, l, dst) in automate["transitions"] if src == etat and l == lettre]
            if len(cibles) > 1:
                print(f"Non déterministe : depuis l'état {etat} avec '{lettre}' -> {cibles}")
                deterministe = False

    if deterministe:
        print("L'automate est déterministe.")
    return deterministe


def est_complet(automate):
    """
    :param automate: un automate pour verifier si il est complet
    :return: True si l'automate est complet (si chaque element de l'alphabet mene a un etat)
    """
    complet = True
    for etat in range(automate["nb_etats"]):
        for lettre in automate["alphabet"]:
            cibles = [dst for (src, l, dst) in automate["transitions"] if src == etat and l == lettre]
            if len(cibles) == 0:
                print(f"Non complet : aucune transition depuis l'état {etat} avec '{lettre}'")
                complet = False

    if complet:
        print("L'automate est complet.")
    return complet


def completion(automate):
    """
    :param automate: automate qu'on veut completer
    :return: l'automate completé (ajout d'un etat poubelle pour les transitions manquantes)
    """
    poubelle = "P"
    poubelle_utilise = False

    for etat in range(automate["nb_etats"]):
        for lettre in automate["alphabet"]:
            cibles = [dst for (src, l, dst) in automate["transitions"] if src == etat and l == lettre]
            if len(cibles) == 0:
                automate["transitions"].append((etat, lettre, poubelle))
                poubelle_utilise = True

    if poubelle_utilise:
        for lettre in automate["alphabet"]:
            automate["transitions"].append((poubelle, lettre, poubelle))
        automate["nb_etats"] += 1

    return automate


def formatter_etat(ensemble):
    """
    :param ensemble: la liste des etats qu'on veux formatter
    :return: le nouvel etat dans le bon format en chaine de charactères
    """
    if ensemble == set({"P"}):
        return "P"
    etats = sorted(ensemble)
    if all(e <= 9 for e in etats):
        return "".join(str(e) for e in etats)
    else:
        return ".".join(str(e) for e in etats)

def fermeture_epsilon(etats, automate):
    fermeture = set(etats)
    pile = list(etats)
    while pile:
        etat = pile.pop()
        for (src, l, dst) in automate["transitions"]:
            if src == etat and l == "e" and dst not in fermeture:
                fermeture.add(dst)
                pile.append(dst)
    return fermeture

def determinisation_et_completion(automate):
    """
    :param automate: automate qu'on veut determiniser
    :return: l'automate determinisé et complété
    """

    initial = fermeture_epsilon(automate["initiaux"], automate)
    etats_a_traiter = [initial]
    etats_traites = []
    nouvelles_transitions = []
    nouveaux_finaux = []

    while etats_a_traiter:
        courant = etats_a_traiter.pop(0)
        if courant in etats_traites:
            continue
        etats_traites.append(courant)

        for e in courant:
            if e in automate["finaux"]:
                nouveaux_finaux.append(courant)
                break

        for lettre in automate["alphabet"]:
            if lettre == "e":
                continue
            cibles = set(
                dst for (src, l, dst) in automate["transitions"]
                if src in courant and l == lettre
            )
            if cibles:
                cibles = fermeture_epsilon(cibles, automate)
            if not cibles:
                cibles = set({"P"})
            nouvelles_transitions.append((courant, lettre, cibles))
            if cibles not in etats_traites and cibles not in etats_a_traiter:
                etats_a_traiter.append(cibles)

    poubelle = set({"P"})
    if poubelle not in etats_traites:
        etats_traites.append(poubelle)
        for lettre in automate["alphabet"]:
            if lettre != "e":
                nouvelles_transitions.append((poubelle, lettre, poubelle))

    alphabet_sans_epsilon = [l for l in automate["alphabet"] if l != "e"]

    return {
        "nb_etats": len(etats_traites),
        "alphabet": alphabet_sans_epsilon,
        "initiaux": [formatter_etat(initial)],
        "finaux": [formatter_etat(e) for e in nouveaux_finaux],
        "transitions": [(formatter_etat(src), l, formatter_etat(dst)) for (src, l, dst) in nouvelles_transitions]
    }

def afficher_automate(automate):
    """
    :param automate: l'automate qu'on veut afficher
    :return: rien
    """
    print(f"Nombre d'états : {automate['nb_etats']}")
    print(f"Alphabet       : {automate['alphabet']}")
    print(f"Initiaux       : {automate['initiaux']}")
    print(f"Finaux         : {automate['finaux']}")
    print("Transitions    :")
    for (src, lettre, dst) in automate["transitions"]:
        print(f"  {src} --{lettre}--> {dst}")


def determiniser_et_completer(AF):
    """
    :param AF: l'automate qu'on veut determiniser et completer
    :return: verifie si l'automate n'est pas deja determinise ou complet, appelle les fonctions sinon et return l'automate AFDC
    """
    if est_deterministe(AF):
        if est_complet(AF):
            AFDC = AF
        else:
            AFDC = completion(AF)
    else:
        AFDC = determinisation_et_completion(AF)

    print("\nAutomate déterministe et complet (AFDC) :")
    afficher_automate(AFDC)
    return AFDC