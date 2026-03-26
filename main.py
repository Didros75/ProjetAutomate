import utile
import determinisation_completion
import Reconnaissance_de_mot
import standardisation
import langage_complementaire
import mermaid
from utile import txt_dictionnaire


auto = txt_dictionnaire("automates", "31")
utile.afficher_automate(auto)
"""auto = determinisation_completion.determiniser_et_completer(auto)
utile.afficher_automate(auto)"""

mermaid.exporter_mermaid(determinisation_completion.determiniser_et_completer(auto))