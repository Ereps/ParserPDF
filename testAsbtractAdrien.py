import fitz

#Partie de base pour extraire un pdf en txt

fname = "Corpus_test/Torres-moreno1998.pdf"  # get document filename
outputFname = "Corpus_result/torres-moreno" + ".txt"

with fitz.open(fname) as doc:  # open document
    pageTest = doc.load_page(0)
    text = pageTest.get_blocks()
with open(outputFname,'w') as file:
    #print(doc.metadata)
    file.write(text)

#Partie : comment single out l'abstract
    
