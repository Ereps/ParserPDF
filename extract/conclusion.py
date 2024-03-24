import re
from extract.block_treatement import *

"""
il n'y a pas forcément de conclusion, sa position dans le doc change selon la présence ou non d'appendix, acknowledgments, discussion (peut être avant ou après)
le titre est toujours composé de "conclusion" ou "c onclusion"
il y a un cas où en remontant le texte à l'envers, le premier "conclusion" trouvé n'est pas celui du titre de la partie conclusion : jing-cutepaste. dans ce cas le "conclusion" est dans la partie Acknowledgments
note : faut ignorer appendix, future work, acknowledgment pour la sortie

edit : délimiter la section conclusion
section possible à la suite : Acknowledgements | References | Acknowledgment | R EFERENCES | Follow-Up Work | ACKNOWLEDGMENT | Appendix

POUR CORRIGER TORRES : y'a References dans le titre qui gêne avec le regex, donc gérer de la même manière que biblio ?
"""
#TODO virer le potentiel chiffre à la fin de conclu (exemple avec Iria_Juan-Manuel)

def extract(blocks, doc):
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

    """Extracts conclusion from a list of text blocks."""
    conclu_string = ""
    conclu_index = 0
    concludebut_pattern = re.compile(r'(Conclusions|Conclusion|ONCLUSION|ONCLUSIONS)')
    conclufin_pattern = re.compile(r'(Acknowledgements|References|Acknowledgment|EFERENCES|Follow-Up Work|ACKNOWLEDGMENT|Appendix)')

    # Check if any of the conclusion patterns are in the title
    title_has_conclusion = bool(re.search(concludebut_pattern, title))

    if not title_has_conclusion:
        # If conclusion pattern is not in the title, search from the end
        for i in range(len(blocks)-1, -1, -1):
            block_text = replace_special_char(blocks[i][4])
            conclu_match = concludebut_pattern.search(block_text)
        
            if conclu_match:
                conclu_index = i
                # Finding the index of the end pattern
                for j in range(i, len(blocks)):
                    end_match = conclufin_pattern.search(replace_special_char(blocks[j][4]))
                    if end_match:
                        # Extract text from conclu_match.start() to end_match.start()
                        conclu_string = replace_special_char(" ".join([block[4] for block in blocks[i:j]]))
                        return conclu_string, conclu_index

                # If end pattern is not found till the end, return all text from current match
                conclu_string = replace_special_char(" ".join([block[4] for block in blocks[i:]]))
                return conclu_string, conclu_index

    else:
        # If conclusion pattern is in the title, check each block
        for i in range(len(blocks)):
            block_text = replace_special_char(blocks[i][4])
            conclu_match = concludebut_pattern.search(block_text)
            
            if conclu_match:
                # If conclusion pattern is found, check if this block contains the title
                if re.search(title, block_text, re.IGNORECASE):
                    # If title is found in this block, skip it and continue
                    continue
                
                # If title is not found, extract conclusion from this block
                conclu_index = i
                conclu_string = replace_special_char(block_text[conclu_match.start():])
                
                # Continue adding text to conclu_string until the end of the block
                while i + 1 < len(blocks) and block_text[-1] != ".":
                    i += 1
                    conclu_string += replace_special_char(blocks[i][4])
                
                break  # Stop searching after finding the first occurrence
    
    return conclu_string, conclu_index