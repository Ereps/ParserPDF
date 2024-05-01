import re, fitz
from extract.block_treatement import replace_special_char

def ADcheck(pdf) -> None :
    pattern = re.compile(r'.*(Elsevier).*')
    with fitz.open(pdf) as doc :
        page = doc.load_page(0)
        text = page.get_textpage()
        if pattern.match(text.extractText()) :
            #print("BRGH")
            doc.delete_page(0)
            doc.saveIncr()
    