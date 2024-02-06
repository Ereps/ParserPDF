#! /usr/bin/env python
#coding: utf-8

import pathlib, fitz,time
import glob, os


output_name = "sortie/"
input_name="Corpus_test/"

#Lire les fichiers pdf
def readfiles(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
       pdfs.append(file)
    return pdfs




startTime = time.time()
pdf_list = readfiles(input_name)
print(os.getcwd())
if(pathlib.Path(output_name).exists()):
    pathlib.Path(output_name).rmdir()
pathlib.Path(output_name).mkdir(parents=True, exist_ok=True)

fname = ""  # get document filename
outputFname = "" + ".txt"

for pdf in pdf_list:
    fname = pdf
    outputFname = output_name +fname + ".txt"
    #print(fname)
    with fitz.open(fname) as doc:  # open document
        pageTest = doc.load_page(0)
        text = pageTest.get_text()
    with open(outputFname,'w') as file:
        #print(doc.metadata)
        file.write(text)


print("--- %s seconds ---" % (time.time() - startTime))

#text = chr(12).join([page.get_text() for page in doc])
# write as a binary file to support non-ASCII characters
#pathlib.Path("Corpus_result/Boudin-Torres-2006" + ".txt").write_bytes(text.encode())
