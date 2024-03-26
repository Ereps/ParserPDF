from extract.block_treatement import *

"""récupération du titre du pdf"""
#TODO extraction du titre avec la taille de police plutot qu'a la louche
def extract(blocks: list, doc: open) -> str :
    title = ""
    i = 0
    title_block = 0
    if doc.metadata.get("title") != "": #si le titre apparaît dans la metadata
        txt = ""
        block_text = replace_special_char(blocks[i][4])
        if "<" in block_text: #si le premier paragraphe commence par un "<"
            i += 1
        title_block = i
        txt = replace_special_char(blocks[i][4])
        i += 1
        if txt.rstrip(" ") == doc.metadata.get("title"): #si le titre est égal au paragraphe récupéré
            title = txt
        else: #sinon
            title_block = i
            txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
            title = txt.rstrip(" ") #on enlève le dernier espace du titre
    else: #si le titre n'est pas dans les metadatas
        #TODO trouver une solution avec la police d'écriture
        title_block = i
        txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
        title = txt

    title = title.replace('\n', '')
    title = title.strip()
    return title
