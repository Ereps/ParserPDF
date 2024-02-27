import re
from extract.block_treatement import *

def extract(blocks, title, abstract_index):
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
        if title in blocks[x][4]:
            index = x+1
            break
    for i in range(index, abstract_index, 1):
        block_text = replace_special_char(blocks[i][4]) #remplace tous les accents
        author_match = author_pattern.search(block_text) #cherche les auteurs
        email_match = email_pattern.search(block_text) #cherche les mails
        semi_mail_match = semi_mail_pattern.search(block_text) #cherche les fins de mails
        print(block_text)
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