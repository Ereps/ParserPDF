import re
from block_treatement import *

#TODO extract-intro
def extract(blocks):
    intro_string = ""
    return intro_string

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