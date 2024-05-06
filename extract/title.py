import re, fitz
from extract.block_treatement import *

"""récupération du titre du pdf"""
#TODO extraction du titre avec la taille de police plutot qu'a la louche
def extract(blocks: list, doc: fitz.open, index_begin: int) -> tuple[str, int] :
    title = ""
    if doc.metadata.get("title") != "" : #si le titre apparaît dans la metadata
        #print('BRGH')
        pattern = re.compile(r"(%s).*" % doc.metadata.get('title'))
        #print(doc.metadata.get("title"))
        for i in range(index_begin, len(blocks)) :
            block_text = replace_special_char(blocks[i][4])
            #print(block_text)
            if pattern.match(block_text) :
                return block_text, i+1
    else: #si le titre n'est pas dans les metadatas
        #TODO trouver une solution avec la police d'écriture
        title = replace_special_char(blocks[index_begin][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
        #print(title, index_begin)

    title = title.replace('\n', '')
    title = title.strip()
    #print('Title ', i)
    return title, 0
