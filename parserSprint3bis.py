import pathlib
import fitz
import glob
import os
import linecache as lc
import time
import re
from extract import abstract,title,authors,block_treatement,biblio, authors_emails
output_name = "sortie/"
input_name = "Corpus_test/"

# Function to read PDF files
def read_files(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
        pdfs.append(file)
    return pdfs

# Function to remove directory
def rmdir(directory):
    directory = pathlib.Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()






startTime = time.time()
pdf_list = read_files(input_name)
print(os.getcwd())
if pathlib.Path(output_name).exists():
    rmdir(output_name)
pathlib.Path(output_name).mkdir(parents=True, exist_ok=True)

def remove_before_pdf_file(text):
    match = re.search(r'PDF File', text)
    if match:
        return text[match.start():]
    else:
        return text

def clear_file(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('')

for pdf in pdf_list:
    fname = pdf
    outputFname = output_name + fname + ".txt"
    print(fname)
    text = ""
    with fitz.open(fname) as doc:  # open document
        blocks=  [] #list of all the text blocks
        dict_blocks = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
            """dict_blocks += page.get_text("dict")["blocks"]
            #TODO work with blocks, not the text
            for b in blocks:
                #print(b)
                text += b[4] + "\n"  # Concatenate text from each block with a newline character
            for i in dict_blocks:
                for j in i["lines"]:
                    for k in j["spans"]:
                        print(k["text"])
                print("\n\n")"""
        
        #nomalization_______________________________
        normal_blocks = block_treatement.blocks_normalization(blocks)

        with open(outputFname+"test.txt",'w', encoding='utf-8') as file:
            for b in normal_blocks:
                #print(b)
                file.write("________________________________"+b[4])
        with open(outputFname,'w', encoding='utf-8') as file:
            #print(doc.metadata)
            pathlib.Path(outputFname).write_bytes(text.encode())
            file.write(text)

        with open(outputFname, 'a', encoding='utf-8') as output:
            output.write("PDF File: " + pdf + "\n")

            
            # Extract and write title
            title_text,title_index = title.extract(normal_blocks, doc)
            output.write("Title: " + title_text + "\n")
            
            
            # Extract and write abstract
            abstract_text,abstract_index= abstract.extract(normal_blocks)
            print(abstract_index)
            author_email_list = authors_emails.extract(normal_blocks, title_text, abstract_index)
            authors_text = ""
            for author in author_email_list:
                authors_text += author[0] + ", "
            output.write("Authors: " + authors_text[:-2] + "\n")
            output.write("Abstract: " + abstract_text + "\n")

            biblio_text, biblio_index= biblio.extract(normal_blocks, title.extract(normal_blocks, doc)[0])
            output.write(biblio_text + "\n")
            clear_file(outputFname)

            new_text = remove_before_pdf_file(outputFname)
            output.write(new_text)

print("--- %s seconds ---" % (time.time() - startTime))
