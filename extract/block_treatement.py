import re

def templateSubtitle(blocks: list) -> str :
    pattern = re.compile(r'((I.)|(1.)|(1)) ([I][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn])')
    for i in range(len(blocks)) :
        block_text = replace_special_char(blocks[i][4])
        if pattern.match(block_text) :
            texts = block_text.split(' ')
            if texts[0] == "1." :
                return "C."
            elif texts[0] == "I." :
                return "L."
            else :
                return "C"
    return ""

def make_uchr(code: str) -> str :
    return chr(int(code.lstrip("U+").zfill(8), 16))

#return the normalize version of the text blocks
def blocks_normalization(blocks : list) -> list :
    normal_blocks = []
    #tuple to list
    normal_blocks = [list(item) for item in blocks]
    #normalize
    for i in range(len(normal_blocks)):
        normal_blocks[i][4] = replace_special_char(normal_blocks[i][4])
    return normal_blocks

def replace_special_char(text : str) -> str :
    text = text.strip()
    continus_word = re.compile(r'-( )*\n')
    text = re.sub(continus_word,"",text)
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('- ', '')
    text = text.replace('`A', 'À')
    text = text.replace('^A', 'Â')
    text = text.replace('"A', 'Ä')
    text = text.replace('´E', 'É')
    text = text.replace('`E', 'È')
    text = text.replace('¨E', 'Ë')
    text = text.replace('^E', 'Ê')
    text = text.replace('´E', 'É')
    text = text.replace('¨I', 'Ï')
    text = text.replace('^I', 'Î')
    text = text.replace('`I', 'Ì')
    text = text.replace('`U', 'Ù')
    text = text.replace('¨U', 'Ü')
    text = text.replace('`¨U', 'Ǜ')
    text = text.replace('^U', 'Û')
    text = text.replace('`O', 'Ò')
    text = text.replace('¨O', 'Ö')
    text = text.replace('^O', 'Ô')
    text = text.replace('`Y', 'Ỳ')
    text = text.replace('¨Y', 'Ÿ')
    text = text.replace('^Y', 'Ŷ')
    text = text.replace('^Z', 'Ẑ')
    text = text.replace('^S', 'Ŝ')
    text = text.replace('^G', 'Ĝ')
    text = text.replace('^H', 'Ĥ')
    text = text.replace('¨H', 'Ḧ')
    text = text.replace('^J', 'Ĵ')
    text = text.replace('¨W', 'Ẅ')
    text = text.replace('^W', 'Ŵ')
    text = text.replace('`W', 'Ẁ')
    text = text.replace('^C', 'Ĉ')
    text = text.replace('¨X', 'Ẍ')
    text = text.replace('`N', 'Ǹ')
    text = text.replace('´e', 'é')
    text = text.replace('`e', 'è')
    text = text.replace('^e', 'ê')
    text = text.replace('"e', 'ë')
    text = text.replace('"a', 'ä')
    text = text.replace('a¨', 'ä')
    text = text.replace('¨a', 'ä')
    text = text.replace('^a', 'â')
    text = text.replace('`a', 'à')
    text = text.replace('´a', 'á')
    text = text.replace('°a', 'å')
    text = text.replace('"ı', 'ï')
    text = text.replace('ı¨', 'ï')
    text = text.replace('ˆı', 'î')
    text = text.replace('`ı', 'ì')
    text = text.replace('`u', 'ù')
    text = text.replace('`¨u', 'ǜ')
    text = text.replace('"u', 'ü')
    text = text.replace('^u', 'û')
    text = text.replace('`o', 'ò')
    text = text.replace('"o', 'ö')
    text = text.replace('^o', 'ô')
    text = text.replace('`y', 'ỳ')
    text = text.replace('"y', 'ÿ')
    text = text.replace('^y', 'ŷ')
    text = text.replace('´y', 'ý')
    text = text.replace('^z', 'ẑ')
    text = text.replace('^s', 'ŝ')
    text = text.replace('^g', 'ĝ')
    text = text.replace('^h', 'ĥ')
    text = text.replace('"h', 'ḧ')
    text = text.replace('^j', 'ĵ')
    text = text.replace('`w', 'ẁ')
    text = text.replace('^w', 'ŵ')
    text = text.replace('"w', 'ẅ')
    text = text.replace('^c', 'ĉ')
    text = text.replace('c¸', 'ç')
    text = text.replace('"t', 'ẗ')
    text = text.replace('"x', 'ẍ')
    text = text.replace('`n', 'ǹ')
    text = text.replace('ﬁ', 'fi')
    # XML cid(?) TIME
    text = text.replace(' ⃗', '~')
    text = text.replace('(⃗', '(~')
    text = text.replace('’', '\'')
    text = text.replace('′', '\'')
    text = text.replace('', 'cid(?)')
    text = text.replace('f', 'cid(?)')
    #traitement xml
    text = text.replace('', 'cid(?)')
    text = text.replace('<', 'cid(?)')
    text = text.replace('>', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('&', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')
    text = text.replace('', 'cid(?)')


    return text


def suppr_special_char(text : str) -> str :
    text = text.strip()
    continus_word = re.compile(r'-( )*\n')
    text = re.sub(continus_word,"",text)
    text = text.replace('é', 'e')
    text = text.replace('è', 'e')
    text = text.replace('ê', 'e')
    text = text.replace('ë', 'e')
    text = text.replace('ä', 'a')
    text = text.replace('â', 'a')
    text = text.replace('à', 'a')
    text = text.replace('á', 'a')
    text = text.replace('å', 'a')
    text = text.replace('ï', 'i')
    text = text.replace('î', 'i')
    text = text.replace('ì', 'i')
    text = text.replace('ù', 'u')
    text = text.replace('ǜ', 'u')
    text = text.replace('ü', 'u')
    text = text.replace('û', 'u')
    text = text.replace('ò', 'o')
    text = text.replace('ö', 'o')
    text = text.replace('ô', 'o')
    text = text.replace('ỳ', 'y')
    text = text.replace('ÿ', 'y')
    text = text.replace('ŷ', 'y')
    text = text.replace('ý', 'y')
    text = text.replace('ẑ', 'z')
    text = text.replace('ŝ', 's')
    text = text.replace('ĝ', 'g')
    text = text.replace('ĥ', 'h')
    text = text.replace('ḧ', 'h')
    text = text.replace('ĵ', 'j')
    text = text.replace('ẁ', 'w')
    text = text.replace('ŵ', 'w')
    text = text.replace('ẅ', 'w')
    text = text.replace('ĉ', 'c')
    text = text.replace('ç', 'c')
    text = text.replace('ẗ', 't')
    text = text.replace('ẍ', 'x')
    text = text.replace('ǹ', 'n')

    return text

"""
boudin-torres-2006
c⃝ -> en fait même avec ça, ça passe



das_martins

<

gonzalez



&

torres-moreno
                                    
"""