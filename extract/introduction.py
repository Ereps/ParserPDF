import re
from extract.block_treatement import *
from extract.abstract import getStartAbs

def getStart(blocks: list) -> int :
    for i in range(getStartAbs(blocks), len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'(.*([I][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]))|(1|I).*') #|(1|I).*
        if pattern.match(block_text) :
            #print("Intro", i)
            return i

def getEnd(blocks: list) -> int :
    for i in range(getStart(blocks), len(blocks)) :
        text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'(2|I{2})(\ \.)?([A-Z][a-z])*')
        if pattern.match(text) :
            #print(i)
            return i
        
def toString(blocks: list) -> str :
    intro_index = getStart(blocks)
    end_index = getEnd(blocks)
    #print(intro_index, end_index)
    string = ""
    for i in range(intro_index, end_index) :
        string += blocks[i][4] + " "
    #print(string)
    return string

"""
notes:
l'intro peut être constituée de un ou plusieurs blocks
il y a toujours le mot clé "Introduction" ou "INTRODUCTION"
les annotations de bas de page (considérées comme un block à part) sont à gérer
si l'introduction est sur plusieurs pages, le haut de page est à gérer
cas: Mikolov.pdf on a [1.1 Goals of the paper et 1.2 Previous work] des sous parties de Introduction ? demander à Mr. Kessler si c'est à mettre dans la partie Introduction ou Corps
idée délimiter partie Introduction : la partie Introduction est tout le temps suivie par 2 | 2. | II. {titre de la partie}, avec une police d'écriture plus grosse que le texte normal (ou en bold parfois)
idée annotations : virer les blocs de taille inférieur à X caractères ?

"""