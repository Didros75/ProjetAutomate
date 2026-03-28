#fonction de minimisation
from itertools import count

from determinisation_completion import est_deterministe, est_complet

def concatList(L) :
    """

    :param L: une liste
    :return: une chaine de caractere string
    """
    strFinal=""
    for i in range(len(L)) :
         strFinal+=str(L[i])
         if i != len(L)-1 :
             strFinal+="."
    return strFinal

def listSub(L1, L2):
    """

    :param L1: une liste
    :param L2: une deuxieme
    :return: une liste
    """
    nL=[]
    for elem in L1 :
        if elem not in L2:
            nL.append(elem)
    return nL

#petite fonction pour clarifier le code, permet de trouver la destination dans l'AFDC
def destination(etat, lettre, transitions):
    """

    :param etat: etat de l'automate
    :param lettre: lettre de l'aphabet de l'automate
    :param transitions: la transition de l'etat a l'automate
    :return:
    """
    for t in transitions:
        if t[0] == etat and t[1] == lettre:
            return t[2]


#les signatures sont la trace des destinations par etat
def signature(etat, alphabet, transitions, partition):
    """

    :param etat: etat de l'automate
    :param alphabet: alphabet
    :param transitions: les transitions
    :param partition: un partition
    :return: un tuple de signature (la trace des groupes d'état)
    """
    s = []
    for l in alphabet:
        d = destination(etat, l, transitions)
        for i, grp in enumerate(partition):
            if d in grp:
                s.append(i)
                break
    return tuple(s)

#Creation d'une partition en partant des signatures de la précédente
def fPartition(partition, alphabet, transitions):
    """

    :param partition: partition de l'autoname (structure de donnée qui traduit chaque étape de minimisation)
    :param alphabet: alphabet de l'automate
    :param transitions: transitions de l'automate
    :return: une nouvelle partition minimisé
    """
    nPartition = []
    for p in partition:
        pS = {}
        for etat in p:
            s = signature(etat, alphabet, transitions, partition)
            if s not in pS:
                pS[s] = []
            pS[s].append(etat)
        for sg in pS.values():
            nPartition.append(sg)
    return nPartition


#minimise
def minimise(AFDC):
    """

    :param AFDC: prend un automate fini deterministe et complet
    :return: retourne un AFDCM (AFDC minimisé)
    """
    #init
    finaux = AFDC['finaux']
    tous_etats = list({t[0] for t in AFDC['transitions']})
    non_finaux = listSub(tous_etats,finaux)
    partition = [finaux, non_finaux]
    partition2=[]
    #algo
    while (len(partition) != len(partition2)):
        partition2 = partition
        partition = fPartition(partition, AFDC['alphabet'], AFDC['transitions'])
    #compil AFDCM
    return create_AFDCM(AFDC,partition)


def create_AFDCM(AFDC, partitionM):
    """

    :param AFDC: prend un automate fini deterministe et complet
    :param partitionM: une partition minimisé
    :return: un AFDCM (AFDC minimisé via la partition)
    """
    AFDCM={}
    associations = {}
    for grp in partitionM :
         for etat in grp :
              associations[etat]=concatList(grp)
    AFDCM['nb_etats'] = len(partitionM)
    AFDCM['alphabet']=AFDC['alphabet']
    AFDCM['initiaux']=[associations[AFDC['initiaux'][i]] for i in range(len(AFDC['initiaux']))]
    AFDCM['finaux']=list({associations[AFDC['finaux'][i]] for i in range(len(AFDC['finaux']))})
    AFDCM['transitions']=[]
    for i in range(len(partitionM)):
         temoin=partitionM[i][0]
         for transi in AFDC['transitions'] :
            if temoin == transi[0]:
                AFDCM['transitions'].append((associations[temoin],transi[1],associations[transi[2]]))
    return AFDCM