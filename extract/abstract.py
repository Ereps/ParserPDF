import re
from extract.block_treatement import *

#TODO return l'indice des blocks de text au lieu du text en lui meme, comme ca on peut les utilisers pour baliser le champ auteurs(entre celui du titre et celui ce l'abstract)
#TODO faire une autre méthode qui += tout les blocks avec leurs indices 
def extract(blocks):
    """_______________________________________________________________________________________________________"""
    #TODO modif pl
    abstract_string = ""
    abstract_index = 0
    abstract_pattern = re.compile(r'(Abstract|ABSTRACT)')
    for i in range(len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        abstract_match = abstract_pattern.search(block_text)
        #si le mot clef abstract extiste
        if(abstract_match):
            #print("____________________________\n\n\n",block_text) TODO remove
            words = block_text.split()
            #if the blocks have the abstract content
            if(len(words) > 5):
                #si le block contient le texte du abstract
                #remove the abstract in the text
                abstract_index = i
                remove_pattern = re.compile(r'(Abstract|ABSTRACT)(\.| |_|\\|-|—)*')
                abstract_string = replace_special_char(re.sub(remove_pattern,"",block_text,1))
            else:
                #si le block ne contient pas le texte du abstract
                #passe les blocks vide
                while(blocks[i][4] == ""):
                    i+=1  
                abstract_index = i
                abstract_string = replace_special_char(blocks[i+1][4])
            while(abstract_string[len(abstract_string)-1] != "."):
                abstract_string+= replace_special_char(blocks[i+1][4])
                i+=1
            break
        #si le mot clef abstract n'existe pas
        else:
            print("test")
            pass
    return abstract_string, abstract_index