import re
from extract.block_treatement import *

#TODO modifier la logique pour ne pas avoir à utiliser du regex pour trouver la finn, utiliser les blocks

def extract(blocks: list) -> tuple[str, int] :
    """Extracts discussion from a list of text blocks."""
    discu_string = ""
    discu_index = 0
    discudebut_pattern = re.compile(r'(Discussion)')
    discufin_pattern = re.compile(r'(Acknowledgments|Conclusions|Appendix)')

    for i in range(len(blocks)-1, -1, -1):
        block_text = replace_special_char(blocks[i][4])
        discu_match = discudebut_pattern.search(block_text)
        
        if discu_match:
            discu_index = i
            # Finding the index of the end pattern
            for j in range(i, len(blocks)):
                end_match = discufin_pattern.search(replace_special_char(blocks[j][4]))
                if end_match:
                    # Extract text from discu_match.start() to end_match.start()
                    discu_string = replace_special_char(" ".join([block[4] for block in blocks[i:j]]))
                    return discu_string, discu_index

            # If end pattern is not found till the end, return all text from current match
            discu_string = replace_special_char(" ".join([block[4] for block in blocks[i:]]))
            return discu_string, discu_index

    return discu_string, discu_index