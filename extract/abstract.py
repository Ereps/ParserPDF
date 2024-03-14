import re
from extract import introduction
from extract.block_treatement import *

def extract(blocks):
    abstract_index = []
    abstract_pattern = re.compile(r'([A][Bb][Ss][Tt][Rr][Aa][Cc][Tt])')
    for i in range(len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        abstract_match = abstract_pattern.search(block_text)
        #si le mot clef abstract existe
        if(abstract_match):
            words = block_text.split()
            if(len(words) > 5):
                #si le block contient le texte du abstract
                #remove the abstract in the text
                abstract_index.append(i)
                remove_pattern = re.compile(r'(Abstract|ABSTRACT)(\.| |_|\\|-|—)*')
                abstract_string = replace_special_char(re.sub(remove_pattern,"",block_text,1))
            else:
                #si le block ne contient pas le texte du abstract
                #passe les blocks vide
                while(blocks[i][4] == ""):
                    i+=1  
                abstract_index.append(i)
                abstract_string = replace_special_char(blocks[i+1][4])
                abstract_index.append(i+1)
            #temps que le block n'est pas la fin du abstract
            while(abstract_string[len(abstract_string)-1] != "."):
                if(blocks[i+1][4] != ""):
                    abstract_string+= replace_special_char(blocks[i+1][4])
                    abstract_index.append(i+1)
                i+=1
            break
        #si le mot clef abstract n'existe pas
        else:
            #appel extract title
            introduction_index = introduction.extract(blocks)
            if(introduction_index != 0):
                abstract_index.append(introduction_index-1)
                abstract_string = replace_special_char(blocks[introduction_index-1][4])
                
                #remonter jusqu'a trouver le debut de l'abstract (jusqu'a block avec un majuscule au début)
                i = abstract_index[0]
                while(not(abstract_string[0].isupper()) and i > 0):    
                    i-=1
                    if(blocks[i][4] != ""):
                        abstract_string = replace_special_char(blocks[i][4]) + abstract_string
                        abstract_index.append(i)

                #remettre les indices dans l'ordre
                abstract_index.sort()

            else:
                #si on ne trouve pas l'introduction, on assume que c'est le block 4
                abstract_index.append(4)

    return abstract_string, abstract_index