import pathlib
import fitz
import glob
import os
import linecache as lc
import time
import re

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

def extract_abstract(text):
    # Regex pattern to find "Introduction" or "INTRODUCTION"
    intro_pattern = re.compile(r'Introduction|INTRODUCTION')

    # Regex pattern to find "Abstract" or "ABSTRACT"
    abstract_pattern = re.compile(r'Abstract|ABSTRACT')

    this_pattern = re.compile(r'In this article|This article')

    # Search for the introduction keyword
    intro_match = intro_pattern.search(text)

    if intro_match:
        # Get the index of the introduction keyword
        intro_index = intro_match.start()

        # Initialize abstract string
        abs_rev = ""
        
        # Counter for the number of paragraphs found
        paragraph_count = 0

        # Search backwards from the introduction keyword to find the abstract
        abstract_match = abstract_pattern.search(text[:intro_index])
        this_match = this_pattern.search(text[:intro_index])

        # If abstract keyword found, extract abstract
        if abstract_match:
            abstract_index = abstract_match.start()

            # Extract abstract in reverse order
            abs_rev = text[abstract_index:intro_index]

            #remplacer ce qu'il faut pour de la mise en forme
            abs_rev = abs_rev.replace('\n', ' ')
            abs_rev = abs_rev.replace('Abstract', ' ')
            abs_rev = abs_rev.replace('Abstract.', ' ')
            abs_rev = abs_rev.replace('1', ' ')
            abs_rev = abs_rev.replace('I.', ' ')
            abs_rev = abs_rev.replace('1.', ' ')
            abs_rev = abs_rev.replace('- ', '')

            return abs_rev.strip()  # Return abstract string stripped of leading/trailing whitespaces
        else:
    # Abstract keyword not found, search backward for two paragraphs
            this_index = this_match.start()

            abs_rev = text[this_index:intro_index]

            # Replace newline characters with spaces
            abs_rev = abs_rev.replace('\n', ' ')
            abs_rev = abs_rev.replace('Abstract', ' ')
            abs_rev = abs_rev.replace('Abstract.', ' ')
            abs_rev = abs_rev.replace('1', ' ')
            abs_rev = abs_rev.replace('I.', ' ')
            abs_rev = abs_rev.replace('1.', ' ')
            abs_rev = abs_rev.replace('- ', '')

            return abs_rev.strip()  # Return abstract string stripped of leading/trailing whitespaces


    # If either introduction keyword is not found, return empty string
    return ""

def extract_title(outputFname, doc):
    title = ""
    if doc.metadata.get("title") != "":
        txt = ""
        line = " "
        i = 1
        if "<" in lc.getline(outputFname, i):
            i += 1
        while line != "":
            line = lc.getline(outputFname, i).rstrip("\n")
            txt += line + " "
            i += 1
        if txt.rstrip(" ") == doc.metadata.get("title"):
            title = txt
        else:
            txt = " "
            line = " "
            while line != "":
                line = lc.getline(outputFname, i).rstrip("\n")
                txt += line + " "
                i += 1
            title = txt.rstrip(" ")
    else:
        txt = ""
        line = " "
        i = 1
        while line != "":
            line = lc.getline(outputFname, i).rstrip("\n")
            txt += line
            i += 1
        title = txt
    
    return title

def extract_authors(full_text, title_text, abstract):
    # Find the index of the title text in the full text
    title_index = full_text.find(title_text)

    # Find the index of the abstract text in the full text
    abstract_index = full_text.find(abstract)

    # Extract the section between the title and the abstract
    authors_section = full_text[title_index + len(title_text):abstract_index]

    # Return the extracted authors section
    authors_section = authors_section.strip()
    authors_section = authors_section.replace('\n', ' ')
    authors_section = authors_section.replace('- ', '')

    # Return the extracted authors section
    return authors_section


startTime = time.time()
pdf_list = read_files(input_name)
print(os.getcwd())
if pathlib.Path(output_name).exists():
    rmdir(output_name)
pathlib.Path(output_name).mkdir(parents=True, exist_ok=True)

for pdf in pdf_list:
    fname = pdf
    outputFname = output_name + fname + ".txt"
    print(fname)
    text = ""
    with fitz.open(fname) as doc:  # open document
        for page_num in range(1):
            page = doc.load_page(page_num)
            blocks = page.get_text_blocks()

            for b in blocks:
                text += b[4] + "\n"  # Concatenate text from each block with a newline character

        with open(outputFname,'w', encoding='utf-8') as file:
            #print(doc.metadata)
            pathlib.Path(outputFname).write_bytes(text.encode())
            file.write(text)

        with open(outputFname, 'a', encoding='utf-8') as output:
            output.write("PDF File: " + pdf + "\n")

            # Extract and write title
            title_text = extract_title(outputFname, doc)
            output.write("Title: " + title_text + "\n")

            authors_text = extract_authors(text, extract_title(outputFname, doc), extract_abstract(text))
            output.write("Authors: " + authors_text + "\n")

            # Extract and write abstract
            abstract = extract_abstract(text)
            output.write("Abstract: " + abstract + "\n")

print("--- %s seconds ---" % (time.time() - startTime))
