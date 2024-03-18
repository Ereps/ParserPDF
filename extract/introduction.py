import re
from extract.block_treatement import *

#TODO mettre le txt en retour aussi ?
def extract(blocks: list) -> int :
    intro_index = -1
    for i in range(len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        #catch tout les variations d'introduction avec quand meme le I majuscule
        intro_pattern = re.compile(r'([I][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn])')
        intro_match = intro_pattern.search(block_text)
        if intro_match:
            intro_index = i
            break
    #pas introduction trouvé, on cherche intro
    if(intro_index == -1):
        for i in range(len(blocks)):
            block_text = replace_special_char(blocks[i][4])
            intro_pattern = re.compile(r'(Intro|INTRO)')
            intro_match = intro_pattern.search(block_text)
            if intro_match:
                intro_index = i
                break
    return intro_index

def searchEnd(blocks: list) -> int :
    for i in range(len(blocks)) :
        text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'(2|I{2})(\ \.)?([A-Z][a-z])*')
        if pattern.match(text) :
            #print(i)
            return i
        
def toString(blocks: list) -> str :
    intro_index = extract(blocks)
    end_index = searchEnd(blocks)
    string = ""
    for i in range(intro_index+1, end_index) :
        string += blocks[i][4]
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