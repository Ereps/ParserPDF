#! /usr/bin/env python
#coding: utf-8

import pathlib, fitz,time
import glob, os
import linecache as lc


output_name = "sortie/"
input_name="Corpus_test/"

#Lire les fichiers pdf
def readfiles(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
       pdfs.append(file)
    return pdfs

#Remove directory
def rmdir(directory):
    directory = pathlib.Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()



startTime = time.time()
pdf_list = readfiles(input_name)
print(os.getcwd())
if(pathlib.Path(output_name).exists()):
    rmdir(output_name)
pathlib.Path(output_name).mkdir(parents=True, exist_ok=True)

fname = ""  # get document filename
outputFname = "" + ".txt"
text = ""

for pdf in pdf_list:
    fname = pdf
    outputFname = output_name +fname + ".txt"
    print(fname)
    text = ""
    with fitz.open(fname) as doc:  # open document
        for page_num in range(1):
            page = doc.load_page(page_num)
            blocks = page.get_text_blocks()

            for b in blocks:
                text += b[4] + "\n"  # Concatenate text from each block with a newline character

        with open(outputFname,'w', encoding='utf-8') as file:
            print(doc.metadata)
            pathlib.Path(outputFname).write_bytes(text.encode())
            file.write(text)

        with open("../" + "output/" + fname + ".txt", 'w+', encoding="utf-8") as output:
            output.write("PDF File: " + pdf + "\n")
            if doc.metadata.get("title") != "": #si le titre(metadata) n'est pas null
                txt=""
                line=" "
                i = 1
                if "<" in lc.getline(outputFname, i): #si la première ligne n'est pas une image
                    i += 1
                while line != "": #on récupère le premier paragraphe
                    line = lc.getline(outputFname, i).rstrip("\n")
                    txt += line + " "
                    i += 1
                if txt.rstrip(" ") == doc.metadata.get("title"): #si le titre(metadata) est différent du premier paragraphe
                    output.write("Title:    " + txt + "\n")
                else:
                    txt = " "
                    line = " "
                    while line != "": #on récupère le deuxième paragraphe
                        line = lc.getline(outputFname, i).rstrip("\n")
                        txt += line + " "
                        i += 1
                    output.write("Title:    " + txt.rstrip(" ") + "\n")
            else:
                txt = ""
                line = " "
                i = 1
                while line != "": #on récupère le premier paragraphe
                    line = lc.getline(outputFname, i).rstrip("\n")
                    txt += line
                    i += 1
                output.write("Title:    " + txt + "\n")


print("--- %s seconds ---" % (time.time() - startTime))

#text = chr(12).join([page.get_text() for page in doc])
# write as a binary file to support non-ASCII characters
#pathlib.Path("Corpus_result/Boudin-Torres-2006" + ".txt").write_bytes(text.encode())
