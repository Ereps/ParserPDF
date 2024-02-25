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

    return author, email

# TODO: extract email from authors
def extract_email() :
    print()