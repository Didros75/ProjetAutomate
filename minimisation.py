#fonction de minimisation
from itertools import count

from determinisation_completion import est_deterministe, est_complet

def concatList(L) :
    strFinal=""
    for i in range(len(L)) :
         strFinal+=str(L[i])
         if i != len(L)-1 :
             strFinal+="."
    return strFinal

def listSub(L1, L2):
    nL=[]
    for elem in L1 :
        if elem not in L2:
            nL.append(elem)
    return nL

#petite fonction pour clarifier le code, permet de trouver la destination dans l'AFDC
def destination(etat, lettre, transitions):
    for t in transitions:
        if t[0] == etat and t[1] == lettre:
            return t[2]


#les signatures sont la trace des destinations par etat
def signature(etat, alphabet, transitions, partition):
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