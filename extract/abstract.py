import re
from extract.block_treatement import *

def getStartAbs(blocks : list) -> int :
    pattern = re.compile(r'.*([A][Bb][Ss][Tt][Rr][Aa][Cc][Tt]).*')
    for i in range(0, len(blocks)) :
        blocks_text = replace_special_char(blocks[i][4])
        if pattern.match(blocks_text) :
            return i

def getStartIntro(blocks : list) -> int : 
    for i in range(getStartAbs(blocks), len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'(.*([I][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]))|(1|I).*') #|(1|I).*
        if pattern.match(block_text) :
            #print("Intro", i)
            return i

def getAbstract(blocks : list) : 
    remove_pattern = re.compile(r'(Abstract|ABSTRACT)(\.| |_|\\|-|—)*')
    #intro = introduction.getStart(blocks)
    print("Abstract start : ", getStartAbs(blocks))
    abs_i = getStartAbs(blocks)
    block_text = replace_special_char(blocks[abs_i][4])
    if len(block_text) > 8 :
        #print(i)
        block_text = replace_special_char(re.sub(remove_pattern, "", block_text, 1))
        return abs_i+1, block_text
    else :
        string = ""
        for y in range(abs_i+1, getStartIntro(blocks)) : #CHANGE
            string += replace_special_char(blocks[y][4])
        return abs_i+1, string
    # Not found
    #return intro-1, replace_special_char(blocks[intro-1][4])