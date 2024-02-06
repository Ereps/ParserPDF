#! /usr/bin/env python
#coding: utf-8
""""
import fitz

doc = fitz.open("Corpus_test/Gonzalez_2018_Wisebe.pdf") # open a document
doc = fitz.open("Corpus_test/Boudin-Torres-2006.pdf") # open a document

with open("Corpus_result/test_accent.txt", 'w', encoding='utf-8') as fichier_sortie:
    for page in doc: # iterate the document pages
        #text = page.get_text().encode("utf-8")#extract_text().encode('UTF-8') # get plain text (is in UTF-8)
        text = page.get_textpage
        print(text.__annotations__.values)
        #fichier_sortie.write(text) # write text of page
        #fichier_sortie.write('\f') # write page delimiter (form feed 0x0C) bytes((12,))
    fichier_sortie.close() """


import pathlib, fitz,time
"""
vowel = ['a','e','i','o','u','y']
"""
"""import aspose.pdf as ap

input_pdf = fname
output_pdf =  outputFname
# Open PDF document
document = ap.Document(input_pdf)

# Create Text device
textDevice = ap.devices.TextDevice()

# Convert a particular page and save
for v in document.pages:
    textDevice.process(v, output_pdf)

pdf = ironpdf.load(fname)
pdf = ironpdf.PdfDocument.FromFile("sample.pdf")
pdf.SaveAsPdfA("Converted_pdfa.pdf", ironpdf.PdfAVersions.PdfA3)
"""

import glob, os


#Lire les fichiers pdf
def readfiles(path,pdfs):
   os.chdir(path)
   pdfs = []
   for file in glob.glob("*.pdf"):
       print(file)
       pdfs.append(file)





pdfs = []
readfiles("Corpus_test/",pdfs)
startTime = time.time()


"""
fname = "Corpus_test/Boudin-Torres-2006.pdf"  # get document filename
outputFname = "Corpus_result/Boudin-Torres-2006" + ".txt"

with fitz.open(fname) as doc:  # open document
    pageTest = doc.load_page(0)
    text = pageTest.get_text()
with open(outputFname,'w') as file:
    print(doc.metadata)
    file.write(text)
"""
print("--- %s seconds ---" % (time.time() - startTime))

#text = chr(12).join([page.get_text() for page in doc])
# write as a binary file to support non-ASCII characters
#pathlib.Path("Corpus_result/Boudin-Torres-2006" + ".txt").write_bytes(text.encode())
