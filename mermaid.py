def exporter_mermaid(automate, nom_fichier="mermaid.txt"):
    """
    :param automate: automate qu'on veut visualiser sur mermaid
    :param nom_fichier: nom du fichier dans lequel on va l'enregistrer
    :return: ecrit directement dans le fichier
    """
    lignes = []
    lignes.append("---")
    lignes.append("config:")
    lignes.append("  layout: elk")
    lignes.append("  theme: neutral")
    lignes.append("  look: classic")
    lignes.append("---")
    lignes.append("stateDiagram-v2")
    lignes.append("  direction LR")

    for etat in automate["initiaux"]:
        lignes.append(f"    [*] --> {etat}")

    for etat in automate["finaux"]:
        lignes.append(f"    {etat} --> [*]")

    for (src, lettre, dst) in automate["transitions"]:
        lignes.append(f"    {src} --> {dst} : {lettre}")

    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

    print(f"Automate exporté dans {nom_fichier}")