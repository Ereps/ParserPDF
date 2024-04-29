import re
from extract.block_treatement import *

"""récupération du titre du pdf"""
#TODO extraction du titre avec la taille de police plutot qu'a la louche
def extract(blocks: list, doc: open) -> str :
    title = ""
    if doc.metadata.get("title") != "" : #si le titre apparaît dans la metadata
        #print('BRGH')
        pattern = re.compile(r"(%s).*" % doc.metadata.get('title'))
        #print(doc.metadata.get("title"))
        txt = ""
        for i in range(len(blocks)) :
            block_text = replace_special_char(blocks[i][4])
            if pattern.match(block_text) :
                return block_text
    else: #si le titre n'est pas dans les metadatas
        #TODO trouver une solution avec la police d'écriture
        txt = replace_special_char(blocks[0][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
        title = txt

    title = title.replace('\n', '')
    title = title.strip()
    #print('Title ', i)
    return title
