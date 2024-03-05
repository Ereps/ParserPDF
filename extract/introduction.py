import re
from extract.block_treatement import *

#TODO mettre le txt en retour aussi ?
def extract(blocks):
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