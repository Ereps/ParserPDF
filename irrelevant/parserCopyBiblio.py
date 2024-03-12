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

def replace_special_char(text):
    text = text.strip()
    continus_word = re.compile(r'-( )*\n')
    text = re.sub(continus_word,"",text)
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
    text = text.replace('´a', 'á')
    text = text.replace('°a', 'å')
    text = text.replace('"ı', 'ï')
    text = text.replace('ˆı', 'î')
    text = text.replace('`ı', 'ì')
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
    text = text.replace('c¸', 'ç')
    text = text.replace('"t', 'ẗ')
    text = text.replace('"x', 'ẍ')
    text = text.replace('`n', 'ǹ')

    return text

#nomalize every blocks using replace_special_char
def blocks_normalization(blocks):
    normal_blocks = []
    #tuple to list
    normal_blocks = [list(item) for item in blocks]
    #normalize
    for i in range(len(normal_blocks)):
        normal_blocks[i][4] = replace_special_char(normal_blocks[i][4])
    return normal_blocks

#TODO return l'indice des blocks de text au lieu du text en lui meme, comme ca on peut les utilisers pour baliser le champ auteurs(entre celui du titre et celui ce l'abstract)
#TODO faire une autre méthode qui += tout les blocks avec leurs indices 
def extract_abstract(blocks):
    """_______________________________________________________________________________________________________"""
    #TODO modif pl
    abstract_string = ""
    abstract_index = 0
    abstract_pattern = re.compile(r'(Abstract|ABSTRACT)')
    for i in range(len(blocks)):
        block_text = replace_special_char(blocks[i][4])
        abstract_match = abstract_pattern.search(block_text)
        if(abstract_match):
            #print("____________________________\n\n\n",block_text) TODO remove
            words = block_text.split()
            #if the blocks have the abstract content
            if(len(words) > 5):
                #si le block contient le texte du abstract
                #remove the abstract in the text
                abstract_index = i
                remove_pattern = re.compile(r'(Abstract|ABSTRACT)(\.| |_|\\|-|—)*')
                abstract_string = replace_special_char(re.sub(remove_pattern,"",block_text,1))
            else:
                #si le block ne contient pas le texte du abstract
                #passe les blocks vide
                while(blocks[i][4] == ""):
                    i+=1  
                abstract_index = i
                abstract_string = replace_special_char(blocks[i+1][4])
            while(abstract_string[len(abstract_string)-1] != "."):
                abstract_string+= replace_special_char(blocks[i+1][4])
                i+=1
            break
    return abstract_string, abstract_index

"""récupération du titre du pdf"""
#TODO extraction du titre avec la taille de police plutot qu'a la louche
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

    title = title.replace('\n', '')
    title = title.strip()
    return title

def extract_authors(blocks, title, abstract_index):
    author_string = ""
    email = []
    author = []
    author_pattern = re.compile(r'\b[A-Z][a-z]+(?:-[A-Z][a-z]+)?, [A-Z][a-z]+(?:-[A-Z][a-z]+)?\b|\b[A-Z][a-z]+(?:-[A-Z][a-z]+)? [A-Z][a-z]+(?:-[A-Z][a-z]+)?\b')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    semi_mail_pattern = re.compile(r'[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    index = 0
    # Trouver l'indice du bloc contenant le titre
    for x in range(len(blocks)):
        print(x)
        if title in blocks[x][4]:
            index = x+1
            break
    print(index)
    for i in range(index, abstract_index, 1):
        block_text = replace_special_char(blocks[i][4]) #remplace tous les accents
        author_match = author_pattern.search(block_text) #cherche les auteurs
        email_match = email_pattern.search(block_text) #cherche les mails
        semi_mail_match = semi_mail_pattern.search(block_text) #cherche les fins de mails
        print(block_text)
        if(author_match): #si on a trouvé des auteurs
            author.append(author_pattern.findall(block_text)) #ajoute dans la liste auteurs
        if(email_match): #si on a trouvé des mails
            email.append(email_pattern.findall(block_text)) #ajoute dans la liste de mails
        elif(semi_mail_match): # sinon si on a trouvé une fin de mail
            block_text = block_text.replace(' ', '') #on enlève tous les espaces
            print(block_text)
            semi_mail_match = semi_mail_pattern.search(block_text)
            semi_mail_index = semi_mail_match.start() #on cherche où la fin du mail commence
            print(semi_mail_index)
            end_email = semi_mail_pattern.findall(block_text) #on récupère la fin du mail
            mails = ""
            if block_text[(semi_mail_index-1)] == ')':#si l'ensemble des débuts de mails est contenu entre parenthèse
                y = semi_mail_index-2
                while block_text[y] != '(':#on boucle jusqu'à ce qu'on trouve la parenthèse fermante
                    mails = block_text[y] + mails #on récupère le texte dans entre parenthèse
                    y -= 1
                mail_sep = mails.split(',')
                for mail in mail_sep:
                    email.append(mail+end_email[0])
            elif block_text[(semi_mail_index-1)] == '}':#sinon si l'ensemble des débuts de mails est contenu entre chevrons
                y = semi_mail_index-2
                while block_text[y] != '{': #on boucle jusqu'à ce qu'on trouve le chevron fermant
                    mails = block_text[y] + mails #on récupère le texte entre chevrons
                    y -= 1
                mail_sep = mails.split(',')
                for mail in mail_sep:
                    email.append(mail+end_email[0])
            elif block_text[(semi_mail_index-1)] == ']':#sinon si l'ensemble des débuts de mails est contenu entre crochets
                y = semi_mail_index-2
                while block_text[y] != '[':#on boucle jusqu'à ce qu'on trouve le crochet fermant
                    mails = block_text[y] + mails #on récupère le texte entre crochets
                    y -= 1
                mail_sep = mails.split(',') #on sépare le texte grâce aux virgules
                for mail in mail_sep:#boucle sur chaques débuts de mails
                    email.append(mail+end_email[0])#on ajoute le début de mail et la fin à la liste email

    print(author)
    print(email)
    return author, email

    














    """
    # Extraire les paragraphes des auteurs entre le titre et le résumé
    block_text = replace_special_char(blocks[i][4])  # Supposant que replace_special_char est défini

    # Recherche de modèles d'adresses e-mail
    #email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    #emails = email_pattern.findall(block_text)

    # Recherche de modèles de noms d'auteurs
    while(index < abstract_index):

        author_pattern = re.compile(r'\b[A-Z][a-z]+(?:-[A-Z][a-z]+)?, [A-Z][a-z]+(?:-[A-Z][a-z]+)?\b|\b[A-Z][a-z]+(?:-[A-Z][a-z]+)? [A-Z][a-z]+(?:-[A-Z][a-z]+)?\b')  # Pattern pour les noms propres
        authors.extend(author_pattern.findall(block_text))
    
    for a in authors:
        author_string += a + ","
    
    return author_string"""

    """while line:
        buffer.append(line)
        if len(buffer) > len(target_words):
            buffer.pop(0)
        if all(word in ' '.join(buffer) for word in target_words):
            break
        line = file.readline()"""
        
    # Move to the next paragraph
    """while line.strip():  # Skip empty lines
        line = file.readline()"""

    # Read and store characters until a keyword is found
    """while line:
        author_string += line
        line = file.readline()
        if re.search(r'Abstract|In this article|This article', line):
            break"""

#idée de manue : partir de la fin. si on rencontre un "References," vérifier si la ligne = title
# def extract_biblio(text):
#     intro_pattern = re.compile(r'References|REFERENCES')

#     intro_match = intro_pattern.search(text)

#     if intro_match:
#         intro_index = intro_match.start()
#         biblio_string = text[intro_index:]
#         biblio_string = biblio_string.strip()
#         biblio_string = biblio_string.replace('\n', ' ')
#         biblio_string = biblio_string.replace('References', '')
#         biblio_string = biblio_string.replace('REFERENCES', '')
#         biblio_string = biblio_string.replace('- ', '')
#         biblio_string = biblio_string.replace('´e', 'é')
#         biblio_string = biblio_string.replace('`e', 'è')
#         biblio_string = biblio_string.replace('´a', 'à')
#         return biblio_string
    
def extract_biblio(blocks, title):
    """Extracts bibliography from a list of text blocks."""
    biblio_string = ""
    biblio_index = 0
    biblio_pattern = re.compile(r'(References|REFERENCES)')

    # Check if "References" or "REFERENCES" is in the title
    title_has_references = bool(re.search(biblio_pattern, title))

    if not title_has_references:
    # If "References" is not in the title, search from the end
        for i in range(len(blocks)-1, -1, -1):
            block_text = replace_special_char(blocks[i][4])
            biblio_match = biblio_pattern.search(block_text)
        
            if biblio_match:
                biblio_index = i
                # Extract text from biblio_match.start() to the end of the whole text
                biblio_string = replace_special_char(" ".join([block[4] for block in blocks[i:]]))
                break

    else:
        # If "References" is in the title, check each block
        for i in range(len(blocks)):
            block_text = replace_special_char(blocks[i][4])
            biblio_match = biblio_pattern.search(block_text)
            
            if biblio_match:
                # If "References" is found, check if this block contains the title
                if re.search(title, block_text, re.IGNORECASE):
                    # If title is found in this block, skip it and continue
                    continue
                
                # If title is not found, extract bibliography from this block
                biblio_index = i
                biblio_string = replace_special_char(block_text[biblio_match.start():])
                
                # Continue adding text to biblio_string until the end of the block
                while i + 1 < len(blocks) and block_text[-1] != ".":
                    i += 1
                    biblio_string += replace_special_char(blocks[i][4])
                
                break  # Stop searching after finding the first occurrence
    
    return biblio_string, biblio_index


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
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text_blocks()
            #TODO work with blocks, not the text
            for b in blocks:
                #print(b)
                text += b[4] + "\n"  # Concatenate text from each block with a newline character
        
        
        #nomalization_______________________________
        normal_blocks = blocks_normalization(blocks)

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
            title_text = extract_title(outputFname, doc)
            output.write("Title: " + title_text + "\n")

            
            
            # Extract and write abstract
            abstract_text, abstract_index= extract_abstract(normal_blocks)
            #authors_text = 
            extract_authors(normal_blocks, title_text, abstract_index) #TODO modif pl
            #output.write("Authors: " + authors_text + "\n")
            output.write("Abstract: " + abstract_text + "\n")

           # biblio_text = extract_biblio(text)
          #  output.write("References: " + biblio_text + "\n")
            
            biblio_text, biblio_index= extract_biblio(normal_blocks, extract_title(outputFname, doc))
            output.write(biblio_text + "\n")

            clear_file(outputFname)

            new_text = remove_before_pdf_file(outputFname)
            output.write(new_text)

print("--- %s seconds ---" % (time.time() - startTime))
