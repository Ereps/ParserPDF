import re
from extract.block_treatement import *

"""
il n'y a pas forcément de conclusion, sa position dans le doc change selon la présence ou non d'appendix, acknowledgments, discussion (peut être avant ou après)
le titre est toujours composé de "conclusion" ou "c onclusion"
il y a un cas où en remontant le texte à l'envers, le premier "conclusion" trouvé n'est pas celui du titre de la partie conclusion : jing-cutepaste. dans ce cas le "conclusion" est dans la partie Acknowledgments
note : faut ignorer appendix, future work, acknowledgment pour la sortie

edit : délimiter la section conclusion
section possible à la suite : Acknowledgements | References | Acknowledgment | R EFERENCES | Follow-Up Work | ACKNOWLEDGMENT | Appendix
"""

def extract(blocks):
    """Extracts conclusion from a list of text blocks."""
    conclu_string = ""
    conclu_index = 0
    concludebut_pattern = re.compile(r'(Conclusions|Conclusion|C ONCLUSION|C ONCLUSIONS)')
    conclufin_pattern = re.compile(r'(Acknowledgements|References|Acknowledgment|R EFERENCES|Follow-Up Work|ACKNOWLEDGMENT|Appendix)')

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

    return conclu_string, conclu_index