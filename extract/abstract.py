import re
from extract import introduction
from extract.block_treatement import *

def getAbstract(blocks : list) : 
    pattern = re.compile(r'.*([A][Bb][Ss][Tt][Rr][Aa][Cc][Tt]).*')
    remove_pattern = re.compile(r'(Abstract|ABSTRACT)(\.| |_|\\|-|—)*')
    intro = introduction.getStart(blocks)
    #print(replace_special_char(blocks[intro][4]))
    for i in range(0, intro) :
        block_text = replace_special_char(blocks[i][4])
        #print(block_text)
        if pattern.match(block_text) :
            if len(block_text) > 8 :
                #print(i)
                block_text = replace_special_char(re.sub(remove_pattern, "", block_text, 1))
                return i+1, block_text
            else :
                string = ""
                for y in range(i+1, intro) :
                    string += replace_special_char(blocks[y][4])
                return i+1, string
    # Not found
    return intro-1, replace_special_char(blocks[intro-1][4])