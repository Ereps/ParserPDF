import re, fitz
from extract import block_treatement

def ADcheck(pdf) -> tuple[int, int] :
    pattern = re.compile(r'.*(Elsevier).*')
    with fitz.open(pdf) as doc :
        page = doc.load_page(0)
        text = page.get_textpage()
        if pattern.match(text.extractText()) :
            patternBis = re.compile(r".*(Author's personal copy).*")
            page = doc.load_page(1)
            blocks = []
            blocks += page.get_text("blocks")
            blocks = block_treatement.blocks_normalization(blocks)
            for i in range(len(blocks)) :
                block_text = block_treatement.replace_special_char(blocks[i][4])
                if patternBis.match(block_text) :
                    #print('BRGH')
                    #print(block_text, i)
                    return 1, i+1
        return 0, 0
        
            