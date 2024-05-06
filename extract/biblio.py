import re
from extract.block_treatement import *

def extract(blocks : list, doc : open) -> tuple[str, int] :
    """partie title pour ne pas dépendre d'une autre fonction"""
    title = ""
    i = 0
    if doc.metadata.get("title") != "": #si le titre apparaît dans la metadata
        txt = ""
        block_text = replace_special_char(blocks[i][4])
        if "<" in block_text: #si le premier paragraphe commence par un "<"
            i += 1
        txt = replace_special_char(blocks[i][4])
        i += 1
        if txt.rstrip(" ") == doc.metadata.get("title"): #si le titre est égal au paragraphe récupéré
            title = txt
        else: #sinon
            txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
            title = txt.rstrip(" ") #on enlève le dernier espace du titre
    else: #si le titre n'est pas dans les metadatas
        #TODO trouver une solution avec la police d'écriture
        txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
        title = txt

    title = title.replace('\n', '')
    title = title.strip()

    """Extracts bibliography from a list of text blocks."""
    biblio_string = ""
    biblio_index = 0
    biblio_pattern = re.compile(r'(References|REFERENCES)')

    # Check if "References" or "REFERENCES" is in the title
    title_has_references = bool(re.search(biblio_pattern, title))

    if not title_has_references:
    # If "References" is not in the title, search from the end
        for i in range(len(blocks)-1, -1, -1):
            block_text = replace_special_char(blocks[i][4])
            biblio_match = biblio_pattern.search(block_text)
        
            if biblio_match:
                biblio_index = i
                # Extract text from biblio_match.start() to the end of the whole text
                biblio_string = replace_special_char(" ".join([block[4] for block in blocks[i:]]))
                break

    else:
        # If "References" is in the title, check each block
        for i in range(len(blocks)):
            block_text = replace_special_char(blocks[i][4])
            biblio_match = biblio_pattern.search(block_text)
            
            if biblio_match:
                # If "References" is found, check if this block contains the title
                if re.search(title, block_text, re.IGNORECASE):
                    # If title is found in this block, skip it and continue
                    continue
                
                # If title is not found, extract bibliography from this block
                biblio_index = i
                biblio_string = replace_special_char(block_text[biblio_match.start():])
                
                # Continue adding text to biblio_string until the end of the block
                while i + 1 < len(blocks) and block_text[-1] != ".":
                    i += 1
                    biblio_string += replace_special_char(blocks[i][4])
                
                break  # Stop searching after finding the first occurrence
    
    return biblio_string, biblio_index
