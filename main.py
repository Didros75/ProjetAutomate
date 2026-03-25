import utile
import determinisation_completion
import Reconnaissance_de_mot
import standardisation
import langage_complementaire
from utile import txt_dictionnaire

auto = txt_dictionnaire("automates", 44)
auto = determinisation_completion.determiniser_et_completer(auto)
utile.afficher_automate(auto)