# -*- coding: utf-8 -*-


#### PROJET MACHINE A SOUS
### 1ère NSI Pavie 2022-2023
### version corrigée avec assertions au 18/10/2022

import random


symboles = '♠♥♦♣7Ω' ## Symboles utilisés dans le bandit-manchot


def choisir_symbole(symboles : str) -> str :
    """
fonction renvoyant un symbole aléatoire parmi une suite de symbole passée en argument

>>> choisir_symbole('abc') in 'abc'
True
>>> choisir_symbole('abc') in 'def'
False
>>> len(choisir_symbole('abc'))
1
>>> type(choisir_symbole('123456')) == str
True
"""
    assert type(symboles) == str and symboles != "", "Symboles must be a non-empty string"
    return random.choice(symboles)


def fabriquer_chaine(symboles : str , taille : int = 3) -> str :
    """ fonction renvoyant une chaine aléatoire de dimension taille,
à partir de la liste de symbole symboles.

>>> len(fabriquer_chaine('atcg'))
3
>>> len(fabriquer_chaine('atcg', 100))
100
>>> chaine = fabriquer_chaine('atcg')
>>> chaine[0] in 'atcg' and chaine[1] in 'atcg' and chaine[2] in 'atcg'
True
"""

    assert isinstance(symboles, str) and len(symboles) > 0, "symboles must be a non-empty string"
    assert isinstance(taille, int) and taille > 0, "taille must be a positive integer"
    
    chaine = ""           #creation d'une chaine vide
    
    for _ in range(taille) : 
        chaine = chaine + choisir_symbole(symboles)
    return chaine


def compte_symboles_identiques(s : str, chaine: str) -> int :
    """
Fonction renvoyant le nombre d'occurences du symbole s au sein de la chaine chaine
Si le symbole n'est pas présent, renvoie 0

>>> compte_symboles_identiques("a", "abracadabra")
5
>>> compte_symboles_identiques("c", "abracadabra")
1
>>> compte_symboles_identiques("o", "abracadabra")
0
>>> compte_symboles_identiques("a", "")
0
"""
    assert type(s) == str and len(s) == 1, "s must be a string of length 1"
    return chaine.count(s)


def presence_symboles_identiques_multiples(symboles : str, chaine : str) -> bool :
    """ Fonction renvoyant un booléen True si l'un des symboles présent dans
la chaine symboles est présent plusieurs fois dans la chaine chaine, et False sinon

>>> presence_symboles_identiques_multiples('abc', 'abracadabra')
True
>>> presence_symboles_identiques_multiples('abc', 'abcdef')
False
>>> presence_symboles_identiques_multiples('a', 'aaaa')
True
>>> presence_symboles_identiques_multiples('abc', 'efgh')
False

>>> presence_symboles_identiques_multiples('a', '')
False
"""
    
    assert type(symboles) == str and len(symboles) >=1, "symboles must be a non empty string"
    
    for s in symboles :
        if compte_symboles_identiques(s, chaine) >= 2 :
            return True
    return False 


def table_gain(chaine : str, mise: int) -> int:
    """
    Fonction renvoyant le gain selon la chaine passée en argument
    A titre d'information, l'espérance de gain avec la table donnée est de 37.5
>>> table_gain('777', 20)
2000
>>> table_gain('ΩΩΩ', 20)
1000
>>> table_gain('♥♥♥', 10)
200
>>> table_gain('Ω7Ω', 15)
150
>>> table_gain('♠♠7', 10)
50
>>> table_gain('7♠♠', 10)
50
>>> table_gain('♠7♣', 25)
50
>>> table_gain('♠77', 50)
0
    """
    if chaine == "777" :
        return 100*mise
    elif chaine == "ΩΩΩ" :
        return 50*mise
    elif chaine in ['♥'*3, 'Ω'*3, '♠'*3, '♣'*3] :
        return 20*mise
    elif '7' in chaine and presence_symboles_identiques_multiples('Ω', chaine) :
        return 10*mise
    elif '7' in chaine and presence_symboles_identiques_multiples('♠♥♣♦', chaine) :
        return 5*mise
    elif not presence_symboles_identiques_multiples('♠♥♦♣7Ω', chaine) :
        return 2*mise
    else :
        return 0
    
    
def saisir_mise(pot : int) -> int :
    """ Fonction récupérant la mise du joueur / de la joueuse,
     qui doit être un nombre entier compris entre 10 et pot.
     Cette fonction ne peut pas être testée par doctest."""
    
    while True :
        mise = input(f"Mise entre 10 et {pot} : ")
        try :
            mise=int(mise)
        except ValueError :
            print(f"Vous n'avez pas saisi un entier. Veuillez recommencer !")
        else :
            if 10<= mise<= pot :
                break
            else :
                print(f"Votre nombre n'est pas compris entre 10 et {pot}. Veuillez recommencer !")
    return mise
    mise = 0


def demander_continuer() ->  bool :
    """Fonction demandant au joueur / à la joueuse si il/elle souhaite continuer.
    Le joueur/La joueuse doit pouvoir répondre par oui (ou o) ou par non (ou n),
    et la fonction doit être dumbproof.
    Ne peut pas être testée par doctest.
    """
    while True :
        reponse = input(f"Voulez-vous continuer ? o/n  ")
        if reponse.lower() in [ 'y', 'o' ,'yes', 'oui']  :
            return True
        elif reponse.lower() in ['n', 'non', 'no'] :
            return False
        else :
            print(f"Je n'est pas compris : {reponse} ")

                
def afficher_bandit(chaine : str, gain : int) -> None:
    """
    Fonction affichant dans la console le bandit-manchot, avec le tirage obtenu.
    Affiche aussi le gain réalisé.
    Renvoie None.
    Ne peut pas être testée par doctest.
    """
    if gain>0 :
        print(f".............\n|   |   |   |    o\n| {chaine[0]} | {chaine[1]} | {chaine[2]} |   //\n|   |   |   |  //\n............. //\n ")
    else :
        print(f".............\n|   |   |   |    o\n| {chaine[0]} | {chaine[1]} | {chaine[2]} |   //\n|   |   |   |  //\n............. // \n ")
    return None


def demande_nom() -> str :
    """
    Fonction demandant a l'utilisateur son pseudo , il doit etre comprit entre 1 et 10 carracter 
    Ne peut pas être testée par doctest
    """
    while True :
        pseudo = input("Entrez votre pseudo : ")
        if len(pseudo)<11 and len(pseudo)>0 :
            return pseudo
        print("Veuillez recommencer et saisir un pseudo de longeur compris entre 1 et 10")


def main_game() -> int :
    """
    Fonction principale du jeu, qui lance une partie, et se poursuit tant que le joueur /la joueuse
    souhaite ou peut continuer.
    Ne peut pas être testée par doctest.
    """
    pot = 500
    presentation()
    continuer = True
    while continuer  :
        mise = saisir_mise(pot)
        pot = pot - mise
        resultat = fabriquer_chaine(symboles)
        gain = table_gain(resultat, mise)
        pot += gain
        afficher_bandit(resultat, gain)
        print(f"Votre pot actuel est de {pot} ")
        if pot != 0 :
            continuer = demander_continuer()
            if pot<500 :
                print(f"Vous repartez avec {500-pot}  de moins")
            elif pot == pot - mise :
                print("Vous n'avez rein gagné !")
            else :
                print(f"Vous avez gagné {pot-500} ")
            
        else :
            continuer = False
            print("Vous n'avez plus d'argent ! Vous ne pouvez plus jouer ! à une prochaine fois :)")
    if pot>0 :
        sauve_score(demande_nom(), pot)
    print(get_score())


def presentation() -> None :
    """ fonction affichant la présentation, et donnant les règles du jeu"""
    print("\n"*50)
    print("""
##############################################
#                                            #
#              Bandit Manchot                #
#                                            #
# 1ère NSI 2022-2023                         #
##############################################
""")
    print("\n"*5)
    print("Vous disposez d'un capital de départ de 500 € pour jouer au bandit manchot !")
    print("\n"*2)
    input("(Appuyez sur la touche Entrée...) ")


def sauve_score(nom_j : str, score_j: int) -> None :
    """ Fonction sauvant le nom du joueur/de la joueuse, ainsi que son score, dans un fichier texte
nommé HighScore.txt, situé dans le même dossier que ce fichier python
"""
    try :
        with open('HighScore.txt',"r", encoding="utf-8") as f :
            lines = f.readlines()
            hs = [{"nom":"", "score" : 0}]*9
            for i, l in enumerate(lines) :
                nom, score = l.split(" / ")
                try :
                    hs[i] = {"nom" : nom, "score" : int(score)}
                except ValueError :
                    hs[i] = {"nom" : nom, "score" :0}
            is_better_than = len(hs)-1
            while is_better_than>=0 and score_j>hs[is_better_than]['score'] :                    
                if is_better_than != len(hs)-1 :
                    hs[is_better_than+1] = hs[is_better_than]
                hs[is_better_than] = {"nom" : nom_j, "score" : score_j}
                is_better_than -= 1
    except FileNotFoundError :
            hs =[{"nom" : nom_j, "score" : score_j}]
    finally :
        with open("HighScore.txt", "w", encoding="utf8") as f :
            for s in hs :
                if s is not None :
                    f.write(f"{s['nom']} / {s['score']}\n")
                else :
                    f.write(f"Inconnu / 0\n")
                    
def get_score() -> str:
    """ Fonction récupérant les HighScore sauvegardés depuis un fichier HishScore.txt,
et qui renvoie une chaine de caractères correctement formatée pour la console"""
    lines =""
    try :
        with open('HighScore.txt',"r", encoding="utf-8") as f  :
            lines = f.readlines()        
    except FileNotFoundError :
        lines = "Inconnu / 0\n"*9                
    finally :
        HS = [{'nom': line.split(" / ")[0], 'score' : line.split(" / ")[1].replace("\n","")} for line in lines]
    final = ""
    for i,d in enumerate(HS) :
        final +=f"{i+1} {d['nom']:>15} : {d['score']:>10} €\n"
    return final    

## La partie ci-dessous n'est effectuée que si vous déclenchez le programme
## en tant que programme principal (notion de modules, vue en terminale)

if __name__ == "__main__" :
    import doctest
    doctest.testmod()
    main_game()