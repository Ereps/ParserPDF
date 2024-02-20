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
        paragraph_count = 0 # TODO USELESS

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

'''récupération du titre du pdf'''
def extract_title(outputFname, doc):
    title = ""
    if doc.metadata.get("title") != "": #si le titre apparaît dans la metadata
        txt = ""
        line = " "
        i = 1
        if "<" in lc.getline(outputFname, i): #si le premier paragraphe commence par un "<"
            i += 1
        while line != "": #tant qu'on est pas à la fin du paragraphe
            line = lc.getline(outputFname, i).rstrip("\n") #on récupère la ligne et on enlève le caractère de fin de ligne
            txt += line + " "
            i += 1
        if txt.rstrip(" ") == doc.metadata.get("title"): #si le titre est égal au paragraphe récupéré
            title = txt
        else: #sinon
            txt = " "
            line = " "
            while line != "": #tant qu'on est pas à la fin du paragraphe
                line = lc.getline(outputFname, i).rstrip("\n") #on récupère la ligne et on enlève le caractère de fin de ligne
                txt += line + " "
                i += 1
            title = txt.rstrip(" ") #on enlève le dernier espace du titre
    else: #sinon
        txt = ""
        line = " "
        i = 1
        while line != "": #tant qu'on est pas à la fin du paragraphe
            line = lc.getline(outputFname, i).rstrip("\n") #on récupère la ligne et on enlève le caractère de fin de ligne
            txt += line + " "
            i += 1
        title = txt

    title = title.replace('\n', ' ')
    
    return title

def extract_authors(outputFname, title):
    author_string = ""
    with open(outputFname, 'r', encoding='utf-8') as file:
        # Initialize variables
        line = file.readline()
        # Search for the first occurrence of the three first words of the title
        target_words = title.split()[:3]
        # Initialize a buffer to store lines for searching the target words
        buffer = []
        while line:
            buffer.append(line)
            if len(buffer) > len(target_words):
                buffer.pop(0)
            if all(word in ' '.join(buffer) for word in target_words):
                break
            line = file.readline()
        
        # Move to the next paragraph
        while line.strip():  # Skip empty lines
            line = file.readline()

        # Read and store characters until a keyword is found
        while line:
            author_string += line
            line = file.readline()
            if re.search(r'Abstract|In this article|This article', line):
                break
    

    # Clean author string
    author_string = author_string.strip()
    author_string = author_string.replace('\n', ' ')
    author_string = author_string.replace('- ', '')
    author_string = author_string.replace('`A', 'À')
    author_string = author_string.replace('^A', 'Â')
    author_string = author_string.replace('"A', 'Ä')
    author_string = author_string.replace('`E', 'È')
    author_string = author_string.replace('¨E', 'Ë')
    author_string = author_string.replace('^E', 'Ê')
    author_string = author_string.replace('¨I', 'Ï')
    author_string = author_string.replace('^I', 'Î')
    author_string = author_string.replace('`I', 'Ì')
    author_string = author_string.replace('`U', 'Ù')
    author_string = author_string.replace('¨U', 'Ü')
    author_string = author_string.replace('`¨U', 'Ǜ')
    author_string = author_string.replace('^U', 'Û')
    author_string = author_string.replace('`O', 'Ò')
    author_string = author_string.replace('¨O', 'Ö')
    author_string = author_string.replace('^O', 'Ô')
    author_string = author_string.replace('`Y', 'Ỳ')
    author_string = author_string.replace('¨Y', 'Ÿ')
    author_string = author_string.replace('^Y', 'Ŷ')
    author_string = author_string.replace('^Z', 'Ẑ')
    author_string = author_string.replace('^S', 'Ŝ')
    author_string = author_string.replace('^G', 'Ĝ')
    author_string = author_string.replace('^H', 'Ĥ')
    author_string = author_string.replace('¨H', 'Ḧ')
    author_string = author_string.replace('^J', 'Ĵ')
    author_string = author_string.replace('¨W', 'Ẅ')
    author_string = author_string.replace('^W', 'Ŵ')
    author_string = author_string.replace('`W', 'Ẁ')
    author_string = author_string.replace('^C', 'Ĉ')
    author_string = author_string.replace('¨X', 'Ẍ')
    author_string = author_string.replace('`N', 'Ǹ')
    author_string = author_string.replace('´e', 'é')
    author_string = author_string.replace('`e', 'è')
    author_string = author_string.replace('^e', 'ê')
    author_string = author_string.replace('"e', 'ë')
    author_string = author_string.replace('"a', 'ä')
    author_string = author_string.replace('^a', 'â')
    author_string = author_string.replace('`a', 'à')
    author_string = author_string.replace('°a', 'å')
    author_string = author_string.replace('"i', 'ï')
    author_string = author_string.replace('^i', 'î')
    author_string = author_string.replace('`i', 'ì')
    author_string = author_string.replace('`u', 'ù')
    author_string = author_string.replace('`¨u', 'ǜ')
    author_string = author_string.replace('"u', 'ü')
    author_string = author_string.replace('^u', 'û')
    author_string = author_string.replace('`o', 'ò')
    author_string = author_string.replace('"o', 'ö')
    author_string = author_string.replace('^o', 'ô')
    author_string = author_string.replace('`y', 'ỳ')
    author_string = author_string.replace('"y', 'ÿ')
    author_string = author_string.replace('^y', 'ŷ')
    author_string = author_string.replace('´y', 'ý')
    author_string = author_string.replace('^z', 'ẑ')
    author_string = author_string.replace('^s', 'ŝ')
    author_string = author_string.replace('^g', 'ĝ')
    author_string = author_string.replace('^h', 'ĥ')
    author_string = author_string.replace('"h', 'ḧ')
    author_string = author_string.replace('^j', 'ĵ')
    author_string = author_string.replace('`w', 'ẁ')
    author_string = author_string.replace('^w', 'ŵ')
    author_string = author_string.replace('"w', 'ẅ')
    author_string = author_string.replace('^c', 'ĉ')
    author_string = author_string.replace('"t', 'ẗ')
    author_string = author_string.replace('"x', 'ẍ')
    author_string = author_string.replace('`n', 'ǹ')

    # Return the extracted author information
    return author_string

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

            authors_text = extract_authors(outputFname, extract_title(outputFname, doc))
            output.write("Authors: " + authors_text + "\n")

            # Extract and write abstract
            abstract = extract_abstract(text)
            output.write("Abstract: " + abstract + "\n")

            clear_file(outputFname)

            new_text = remove_before_pdf_file(outputFname)
            output.write(new_text)

print("--- %s seconds ---" % (time.time() - startTime))
