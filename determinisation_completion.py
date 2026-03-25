from main import *

def est_synchrone(automate):
    for lettre in automate["alphabet"]:
        if lettre == "ε":
            return False
    return True

def est_deterministe(automate):
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
    if ensemble == frozenset({"P"}):
        return "P"
    etats = sorted(ensemble)
    if all(e <= 9 for e in etats):
        return "".join(str(e) for e in etats)
    else:
        return ".".join(str(e) for e in etats)


def determinisation_et_completion(automate):
    initial = frozenset(automate["initiaux"])
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
            cibles = frozenset(
                dst for (src, l, dst) in automate["transitions"]
                if src in courant and l == lettre
            )
            if not cibles:
                cibles = frozenset({"P"})
            nouvelles_transitions.append((courant, lettre, cibles))
            if cibles not in etats_traites and cibles not in etats_a_traiter:
                etats_a_traiter.append(cibles)

    poubelle = frozenset({"P"})
    if poubelle not in etats_traites:
        etats_traites.append(poubelle)
        for lettre in automate["alphabet"]:
            nouvelles_transitions.append((poubelle, lettre, poubelle))

    return {
        "nb_etats": len(etats_traites),
        "alphabet": automate["alphabet"],
        "initiaux": [formatter_etat(initial)],
        "finaux": [formatter_etat(e) for e in nouveaux_finaux],
        "transitions": [(formatter_etat(src), l, formatter_etat(dst)) for (src, l, dst) in nouvelles_transitions]
    }


def afficher_automate(automate):
    print(f"Nombre d'états : {automate['nb_etats']}")
    print(f"Alphabet       : {automate['alphabet']}")
    print(f"Initiaux       : {automate['initiaux']}")
    print(f"Finaux         : {automate['finaux']}")
    print("Transitions    :")
    for (src, lettre, dst) in automate["transitions"]:
        print(f"  {src} --{lettre}--> {dst}")


def determiniser_et_completer(AF):
    if est_synchrone(automate) == False:
        print("Determinisation impossible sur un automate asynchrone")
        return AF
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

for i in range(35):
    i_t=str(i+10)
    print(i_t)
    automate = txt_dictionnaire("automates", i_t)
    afficher_automate(automate)
    automate2=determiniser_et_completer(automate)
