import fitz

#Partie de base pour extraire un pdf en txt

fname = "Corpus_test/Torres-moreno1998.pdf"  # get document filename
outputFname = "Corpus_result/torres-moreno" + ".txt"

#with fitz.open(fname) as doc:  # open document
#    pageTest = doc.load_page(0)
#    text = pageTest.get_blocks()
#with open(outputFname,'w') as file:
#    #print(doc.metadata)
#    file.write(text)

#with fitz.open(fname) as doc :
#    page = doc.load_page(0)
#    text = page.get_text()
#with open(outputFname,'w') as file:    
#    file.write(text)

text = ""  # Initialize an empty string to store the text from all pages

with fitz.open(fname) as doc:
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text_blocks()
        
        for b in blocks:
            text += b[4] + "\n"  # Concatenate text from each block with a newline character


with open(outputFname, 'w', encoding='utf-8') as file:
    file.write(text)


#Partie : comment single out l'abstract
    
