import utile
import determinisation_completion
import Reconnaissance_de_mot
import standardisation
import langage_complementaire
import mermaid
from utile import txt_dictionnaire

"""
auto = txt_dictionnaire("automates", "31")
utile.afficher_automate(auto)
auto = determinisation_completion.determiniser_et_completer(auto)
utile.afficher_automate(auto)
mermaid.exporter_mermaid(determinisation_completion.determiniser_et_completer(auto))
"""


PRINT_ORIGINAL = print
FICHIER_TRACE = None


def numero_automate(n):
    if n < 10:
        return "0" + str(n)
    return str(n)

def nom_fichier_trace(n):
    if n < 10:
        return "traces/trace_0" + str(n) + ".txt"
    return "traces/trace_" + str(n) + ".txt"


def print_trace(*args, **kwargs):
    global FICHIER_TRACE

    PRINT_ORIGINAL(*args, **kwargs)

    if FICHIER_TRACE is not None:
        sep = " "
        end = "\n"

        if "sep" in kwargs:
            sep = kwargs["sep"]
        if "end" in kwargs:
            end = kwargs["end"]

        texte = ""
        i = 0
        for arg in args:
            if i > 0:
                texte += sep
            texte += str(arg)
            i += 1

        FICHIER_TRACE.write(texte + end)


def activer_trace():
    if type(__builtins__) == dict:
        __builtins__["print"] = print_trace
    else:
        __builtins__.print = print_trace


def desactiver_trace():
    if type(__builtins__) == dict:
        __builtins__["print"] = PRINT_ORIGINAL
    else:
        __builtins__.print = PRINT_ORIGINAL


def traiter_un_automate(n):

    global FICHIER_TRACE

    FICHIER_TRACE = open(nom_fichier_trace(n), "w", encoding="utf-8")

    print("========================================")
    print("Traitement de l'automate", numero_automate(n))
    print("========================================")
    print("")

    print("1) Lecture de l'automate initial")
    auto = utile.txt_dictionnaire("automates", numero_automate(n))
    utile.afficher_automate(auto)
    print("")

    print("2) Vérification de la standardisation")
    if standardisation.est_standard(auto):
        print("L'automate est standard.")
    else:
        print("L'automate n'est pas standard.")
    print("")

    print("3) Standardisation")
    if not standardisation.est_standard(auto):
        auto = standardisation.standardiser(auto)
    print("")

    print("4) Vérification de la synchronisation")
    if determinisation_completion.est_synchrone(auto):
        print("L'automate est synchrone.")
    else:
        print("L'automate n'est pas synchrone.")
    print("")

    print("5) Vérification du déterminisme")
    if determinisation_completion.est_deterministe(auto):
        print("L'automate est deterministe.")
    else:
        print("L'automate n'est pas deterministe.")
    print("")

    print("6) Vérification de la complétude")
    if determinisation_completion.est_complet(auto):
        print("L'automate est complet.")
    else:
        print("L'automate n'est pas complet.")
    print("")

    print("7) Déterminisation et complétion")
    if determinisation_completion.est_complet(auto):
        auto = determinisation_completion.determiniser_et_completer(auto)
    else:
        auto = determinisation_completion.completion(auto)
        auto = determinisation_completion.determiniser_et_completer(auto)
    print("")
    print("Fin du traitement de l'automate", numero_automate(n))

    FICHIER_TRACE.close()
    FICHIER_TRACE = None



def main():
    activer_trace()
    n = 1
    while n <= 44:
        traiter_un_automate(n)
        n += 1
    desactiver_trace()
    print("\nLes 44 traces ont été générées.")

main()