import pathlib
import fitz
import glob
import os
import linecache as lc
import time
import re

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
def extract_title(blocks, doc):
    title = ""
    i = 0
    if doc.metadata.get("title") != "": #si le titre apparaît dans la metadata
        txt = ""
        line = " "
        block_text = replace_special_char(blocks[i][4])
        if "<" in block_text: #si le premier paragraphe commence par un "<"
            i += 1
        txt = replace_special_char(blocks[i][4])
        i += 1
        if txt.rstrip(" ") == doc.metadata.get("title"): #si le titre est égal au paragraphe récupéré
            title = txt
        else: #sinon
            txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
            title = txt.rstrip(" ") #on enlève le dernier espace du titre
    else: #sinon
        txt = replace_special_char(blocks[i][4]) #on récupère la ligne et on enlève le caractère de fin de ligne
        title = txt

    title = title.replace('\n', '')
    title = title.strip()
    return title

def extract_authors(blocks, title, abstract_index):
    email = []
    author = []
    emails = []
    authors = []
    a = []
    e = []
    no_no_in = False
    author_pattern = re.compile(r'[A-Z][a-zàáâäçèéêëìíîïñòóôöùúûüýÿ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿ]*)?(?: +[A-Zdlaeiouàáâäçèéêëìíîïñòóôöùúûüýÿ.]{0,3})?(?:[.]*)? [A-Z][A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿ-]*)?')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    semi_mail_pattern = re.compile(r'[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    no_no_words = ['Université', 'Bretagne', 'Nord', 'Sud', 'Est', 'Ouest', 'University', 'North', 'South', 'West', 'Laboratoire', 'Laboratory', 'Rennes', 'Informatique', 'Google', 'Inc', 'Fondamentale', 'Marseille', 'France', 'Aix-Marseille', 'Vannes', 'Canada', 'Montréal', 'Polytechnique', 'Mexico', 'Avignon', 'Instituto', 'Ingeniería', 'Institute', 'Institue', 'Linguistics', 'Spain', 'Mexique', 'Espagne', 'Québec', 'Pays', 'Vaucluse', 'Meinajaries', 'Département', 'Centre-ville', 'New York', 'Department', 'Computer', 'Science', 'Columbia', 'Technologies', 'Carnegie', 'Mountain', 'View', 'Ecole', 'Centre', 'Ville', 'Cedex']
    index = 0
    # Trouver l'indice du bloc contenant le titre
    for x in range(len(blocks)):
        #print(x)
        if title in blocks[x][4]:
            print(blocks[x][4])
            index = x+1
            break
    print(index)
    for i in range(index, abstract_index, 1):
        block_text = replace_special_char(blocks[i][4]) #remplace tous les accents
        author_match = author_pattern.search(block_text) #cherche les auteurs
        email_match = email_pattern.search(block_text) #cherche les mails
        semi_mail_match = semi_mail_pattern.search(block_text) #cherche les fins de mails
        #print(block_text)
        if(author_match): #si on a trouvé des auteurs
            a.append(author_pattern.findall(block_text)) #ajoute dans la liste auteurs
        if(email_match): #si on a trouvé des mails
            email.append(email_pattern.findall(block_text)) #ajoute dans la liste de mails
            emails = [element for sous_liste in email for element in sous_liste]
            if len(email) == 1: #si on a qu'un seul mail
                email_match = email_pattern.search(block_text)
                email_index = email_match.start()
                if block_text[email_index-1] == ',' or block_text[email_index-2] == ',': #si jamais on trouve une virgule avant le mail
                    block_text = block_text.replace(' ', '')
                    email_match = email_pattern.search(block_text)
                    email_index = email_match.start()
                    semi_mail_match = semi_mail_pattern.search(block_text)
                    end_email = semi_mail_pattern.findall(block_text)
                    e = block_text.split(',') #on sépare le texte grâce qux virgules
                    for m in e: #on boucle sur les éléments du texte séparé
                        if m != email[0][0]: #si l'élément est différent du mail
                            emails.append(m+end_email[0]) #on l'ajoute à la liste des mails
        elif(semi_mail_match): # sinon si on a trouvé une fin de mail
            block_text = block_text.replace(' ', '') #on enlève tous les espaces
            semi_mail_match = semi_mail_pattern.search(block_text)
            semi_mail_index = semi_mail_match.start() #on cherche où la fin du mail commence
            end_email = semi_mail_pattern.findall(block_text) #on récupère la fin du mail
            mails = ""
            if block_text[(semi_mail_index-1)] == ')':#si l'ensemble des débuts de mails est contenu entre parenthèse
                y = semi_mail_index-2
                while block_text[y] != '(':#on boucle jusqu'à ce qu'on trouve la parenthèse fermante
                    mails = block_text[y] + mails #on récupère le texte dans entre parenthèse
                    y -= 1
                mail_sep = mails.split(',')
                for mail in mail_sep:
                    emails.append(mail+end_email[0])
            elif block_text[(semi_mail_index-1)] == '}':#sinon si l'ensemble des débuts de mails est contenu entre chevrons
                y = semi_mail_index-2
                while block_text[y] != '{': #on boucle jusqu'à ce qu'on trouve le chevron fermant
                    mails = block_text[y] + mails #on récupère le texte entre chevrons
                    y -= 1
                mail_sep = mails.split(',')
                for mail in mail_sep:
                    emails.append(mail+end_email[0])
            elif block_text[(semi_mail_index-1)] == ']':#sinon si l'ensemble des débuts de mails est contenu entre crochets
                y = semi_mail_index-2
                while block_text[y] != '[':#on boucle jusqu'à ce qu'on trouve le crochet fermant
                    mails = block_text[y] + mails #on récupère le texte entre crochets
                    y -= 1
                mail_sep = mails.split(',') #on sépare le texte grâce aux virgules
                for mail in mail_sep:#boucle sur chaques débuts de mails
                    emails.append(mail+end_email[0])#on ajoute le début de mail et la fin à la liste email

    for w in a:
        for x in w:
            author.append(x)

    for y in range(len(author)): #boucle sur la liste auteur
        for z in no_no_words: #boucle sur la liste des mots non voulu
            if z in author[y]: #si un mot non voulu est trouvé dans la string
                no_no_in = True #on passe no_no_in a true
        if no_no_in == False: #si no_no_in est false
            authors.append(author[y]) #on l'ajoute à la liste définitive des auteurs
        no_no_in = False #on remet no_no_in a false

    return authors, emails

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