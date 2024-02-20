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

def replace_accent(text):
    text = text.strip()
    text = text.replace('\n', ' ')
    text = text.replace('- ', '')
    text = text.replace('`A', 'À')
    text = text.replace('^A', 'Â')
    text = text.replace('"A', 'Ä')
    text = text.replace('`E', 'È')
    text = text.replace('¨E', 'Ë')
    text = text.replace('^E', 'Ê')
    text = text.replace('¨I', 'Ï')
    text = text.replace('^I', 'Î')
    text = text.replace('`I', 'Ì')
    text = text.replace('`U', 'Ù')
    text = text.replace('¨U', 'Ü')
    text = text.replace('`¨U', 'Ǜ')
    text = text.replace('^U', 'Û')
    text = text.replace('`O', 'Ò')
    text = text.replace('¨O', 'Ö')
    text = text.replace('^O', 'Ô')
    text = text.replace('`Y', 'Ỳ')
    text = text.replace('¨Y', 'Ÿ')
    text = text.replace('^Y', 'Ŷ')
    text = text.replace('^Z', 'Ẑ')
    text = text.replace('^S', 'Ŝ')
    text = text.replace('^G', 'Ĝ')
    text = text.replace('^H', 'Ĥ')
    text = text.replace('¨H', 'Ḧ')
    text = text.replace('^J', 'Ĵ')
    text = text.replace('¨W', 'Ẅ')
    text = text.replace('^W', 'Ŵ')
    text = text.replace('`W', 'Ẁ')
    text = text.replace('^C', 'Ĉ')
    text = text.replace('¨X', 'Ẍ')
    text = text.replace('`N', 'Ǹ')
    text = text.replace('´e', 'é')
    text = text.replace('`e', 'è')
    text = text.replace('^e', 'ê')
    text = text.replace('"e', 'ë')
    text = text.replace('"a', 'ä')
    text = text.replace('^a', 'â')
    text = text.replace('`a', 'à')
    text = text.replace('°a', 'å')
    text = text.replace('"i', 'ï')
    text = text.replace('^i', 'î')
    text = text.replace('`i', 'ì')
    text = text.replace('`u', 'ù')
    text = text.replace('`¨u', 'ǜ')
    text = text.replace('"u', 'ü')
    text = text.replace('^u', 'û')
    text = text.replace('`o', 'ò')
    text = text.replace('"o', 'ö')
    text = text.replace('^o', 'ô')
    text = text.replace('`y', 'ỳ')
    text = text.replace('"y', 'ÿ')
    text = text.replace('^y', 'ŷ')
    text = text.replace('´y', 'ý')
    text = text.replace('^z', 'ẑ')
    text = text.replace('^s', 'ŝ')
    text = text.replace('^g', 'ĝ')
    text = text.replace('^h', 'ĥ')
    text = text.replace('"h', 'ḧ')
    text = text.replace('^j', 'ĵ')
    text = text.replace('`w', 'ẁ')
    text = text.replace('^w', 'ŵ')
    text = text.replace('"w', 'ẅ')
    text = text.replace('^c', 'ĉ')
    text = text.replace('"t', 'ẗ')
    text = text.replace('"x', 'ẍ')
    text = text.replace('`n', 'ǹ')

    # Return the extracted author information
    return text

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

#idée de manue : partir de la fin. si on rencontre un "References," vérifier si la ligne = title
def extract_biblio(text):
    intro_pattern = re.compile(r'References|REFERENCES')

    intro_match = intro_pattern.search(text)

    if intro_match:
        intro_index = intro_match.start()
        biblio_string = text[intro_index:]
        biblio_string = biblio_string.strip()
        biblio_string = biblio_string.replace('\n', ' ')
        biblio_string = biblio_string.replace('References', '')
        biblio_string = biblio_string.replace('REFERENCES', '')
        biblio_string = biblio_string.replace('- ', '')
        biblio_string = biblio_string.replace('´e', 'é')
        biblio_string = biblio_string.replace('`e', 'è')
        biblio_string = biblio_string.replace('´a', 'à')
        return biblio_string

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
        for page_num in range(len(doc)):
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
            abstract_text = extract_abstract(text)
            output.write("Abstract: " + abstract_text + "\n")

           # biblio_text = extract_biblio(text)
          #  output.write("References: " + biblio_text + "\n")

            clear_file(outputFname)

            new_text = remove_before_pdf_file(outputFname)
            output.write(new_text)

print("--- %s seconds ---" % (time.time() - startTime))
