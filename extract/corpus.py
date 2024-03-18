import re
from extract.block_treatement import *

def getStart(blocks: list) -> int :
    for i in range(len(blocks)) :
        block_text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'(2|I{2})(\ \.)?([A-Z][a-z])*')
        if pattern.match(block_text) :
            return i
    return -1

def getEnd(blocks : list) -> int :
    for i in range(len(blocks)) :
        block_text = replace_special_char(blocks[i][4])
        pattern = re.compile(r'.*(([C][Oo][Nn][Cc][Ll][Uu][Ss][Ii][Oo][Nn][Ss]?)|([D][Ii][Ss][Cc][Uu][Ss][Ss][Ii][Oo][Nn]))')
        #print(block_text)
        if pattern.match(block_text) :
            return i
    return -1

def toString(blocks: list) -> str :
    start_i = getStart(blocks)
    end_i = getEnd(blocks)
    #print(start_i, end_i)
    string = ""
    for i in range(start_i+1, end_i) :
        string += blocks[i][4]
    return string