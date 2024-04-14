import re

from extract.block_treatement import *

def extract(blocks, title, abstract_index) -> list:
    email = []
    author = []
    emails = []
    authors = []
    author_email=[]
    affiliation = {}
    a = []
    e = []
    no_no_in = False
    affil_in = False
    affil = ''
    cpt = 1
    author_pattern = re.compile(r'[A-Z][a-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]*)?(?: +[A-Zdlaeiouàáâäçèéêëìíîïñòóôöùúûüýÿﬁ.]{0,3})?(?:[.]*)? [A-Z][A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ-]*)?')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    semi_mail_pattern = re.compile(r'[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    no_no_words = ['Université', 'Bretagne', 'Nord', 'Sud', 'Est', 'Ouest', 'University', 'North', 'South', 'West', 'Laboratoire', 'Laboratory', 'Rennes', 'Informatique', 'Google', 'Inc', 'Fondamentale', 'Marseille', 'France', 'Aix-Marseille', 'Vannes', 'Canada', 'Montréal', 'Polytechnique', 'Mexico', 'Avignon', 'Instituto', 'Ingeniería', 'Institute', 'Institue', 'Linguistics', 'Spain', 'Mexique', 'Espagne', 'Québec', 'Pays', 'Vaucluse', 'Meinajaries', 'Département', 'Centre-ville', 'New York', 'Department', 'Computer', 'Science', 'Columbia', 'Technologies', 'Carnegie', 'Mountain', 'View', 'Ecole', 'Centre', 'Ville', 'Cedex', 'Scalable', 'Approach', 'Sentence', 'Scoring', 'Multi', 'Document', 'Multi-Document', 'Update', 'Word', 'Representations', 'Vector', 'Space', 'System', 'Demonstrations', 'Processing', 'Tool', 'Matière', 'Condensée', 'Compiled', 'April', 'November', 'January', 'February', 'March', 'May', 'June', 'July', 'August', 'September', 'December']
    index = 0
    # Trouver l'indice du bloc contenant le titre
    for x in range(len(blocks)):
        if title in blocks[x][4]:
            index = x+1
            break
    print(index)
    print(abstract_index)
    #abstract_index[0] == premier abstract block
    for i in range(index, abstract_index, 1):
        if 'Abstract' in blocks[i][4] or 'abstract' in blocks[i][4] or 'ABSTRACT' in blocks[i][4]:
            i += 1
            if abstract_index <= i:
                break
        block_text = replace_special_char(blocks[i][4]) #remplace tous les accents
        author_match = author_pattern.search(block_text) #cherche les auteurs
        email_match = email_pattern.search(block_text) #cherche les mails
        semi_mail_match = semi_mail_pattern.search(block_text) #cherche les fins de mails
        if 'J. Manuel Torres Moreno' in block_text:
            a.append(['J. Manuel Torres Moreno'])
        block_text = block_text.replace('J. Manuel Torres Moreno', '')
        #print(block_text)
        if(author_match): #si on a trouvé des auteurs
            a.append(author_pattern.findall(block_text)) #ajoute dans la liste auteurs

        for w in a:
            for x in w:
                author.append(x)
        a = []

        for y in range(len(author)): #boucle sur la liste auteur
            for z in no_no_words: #boucle sur la liste des mots non voulu
                if z in author[y]: #si un mot non voulu est trouvé dans la string
                    no_no_in = True #on passe no_no_in a true
            if no_no_in == False: #si no_no_in est false
                authors.append(author[y]) #on l'ajoute à la liste définitive des auteurs
            no_no_in = False #on remet no_no_in a false
        author = []
        #print(authors)
        
        #print(block_text)
        for t in authors:
            #print(t)
            block_text = block_text.replace(t, '') #supprime les auteurs du texte
            #print(block_text)

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
                    e = block_text.split(',') #on sépare le texte grâce aux virgules
                    for m in e: #on boucle sur les éléments du texte séparé
                        if m != email[0][0]: #si l'élément est différent du mail
                            emails.append(m+end_email[0]) #on l'ajoute à la liste des mails
        elif(semi_mail_match): # sinon si on a trouvé une fin de mail
            block_text_no_space = block_text.replace(' ', '') #on enlève tous les espaces
            semi_mail_match = semi_mail_pattern.search(block_text_no_space)
            semi_mail_index = semi_mail_match.start() #on cherche où la fin du mail commence
            end_email = semi_mail_pattern.findall(block_text_no_space) #on récupère la fin du mail
            mails = ""
            mails_space = ''
            if block_text_no_space[(semi_mail_index-1)] == ')':#si l'ensemble des débuts de mails est contenu entre parenthèse
                y = semi_mail_index-2
                y_space = y
                while block_text_no_space[y] != '(':#on boucle jusqu'à ce qu'on trouve la parenthèse fermante
                    mails = block_text_no_space[y] + mails #on récupère le texte dans entre parenthèse
                    y -= 1
                mail_sep = mails.split(',')
                mails_space = '('
                for mail in mail_sep:
                    emails.append(mail+end_email[0])
                    mails_space += mail + ', '
                mails_space = mails_space[:-2] + ')'
                block_text = block_text.replace(mails_space, '')
            elif block_text_no_space[(semi_mail_index-1)] == '}':#sinon si l'ensemble des débuts de mails est contenu entre chevrons
                y = semi_mail_index-2
                y_space = y
                while block_text_no_space[y] != '{': #on boucle jusqu'à ce qu'on trouve le chevron fermant
                    mails = block_text_no_space[y] + mails #on récupère le texte entre chevrons
                    y -= 1
                mail_sep = mails.split(',')
                mails_space = '{'
                for mail in mail_sep:
                    emails.append(mail+end_email[0])
                    mails_space += mail + ', '
                mails_space = mails_space[:-2] + '}'
                block_text = block_text.replace(mails_space, '')
            elif block_text_no_space[(semi_mail_index-1)] == ']':#sinon si l'ensemble des débuts de mails est contenu entre crochets
                y = semi_mail_index-2
                y_space = y
                while block_text_no_space[y] != '[':#on boucle jusqu'à ce qu'on trouve le crochet fermant
                    mails = block_text_no_space[y] + mails #on récupère le texte entre crochets
                    y -= 1
                mail_sep = mails.split(',') #on sépare le texte grâce aux virgules
                mails_space = '['
                for mail in mail_sep:#boucle sur chaques débuts de mails
                    emails.append(mail+end_email[0])#on ajoute le début de mail et la fin à la liste email
                    mails_space += mail + ', '
                mails_space = mails_space[:-2] + ']'
                block_text = block_text.replace(mails_space, '')
            block_text = block_text.replace(end_email[0], '')
        for z in emails:
            block_text = block_text.replace(z, '') #supprime les mails du texte
        notWanted = re.compile(r' *[&♮♭*∗]+ *| *[0-9,sthrnd]{3}(?:[()A-Za-z]{3})?(?: +|$)|(?:[(][a-z-,.]*[)])')
        nw = notWanted.findall(block_text)
        for n in nw:
            block_text = block_text.replace(n, '')
        notAffiliation = re.compile(r' *[and,*∗ .]+ *')
        isAffiliation = notAffiliation.fullmatch(block_text)
        if isAffiliation == None:
            ajout = False
            same = True
            for r in authors:
                if r not in affiliation:
                    affiliation[r] = block_text
                    affil_in = True
                    ajout = True
            if ajout == False and cpt < 3:
                affiliations = {}
                v = affiliation[authors[0]]
                for key, value in affiliation.items():
                    if value != v:
                        same = False
                if same:
                    for key, value in affiliation.items():
                        affiliations[key] = value + ' ' + block_text
                    affiliation = affiliations
                    cpt += 1

    print(author)
    print(emails)
    print(affiliation)
        

    for em in emails:
        ema = ''
        for c in em:
            if c == '@' or c == 'Q':
                break
            else:
                ema += c
        cpta = 0
        cpt = 0
        auth=''
        sema = ema
        point = re.compile('^[.]+$')
        for aut in authors:
            for au in aut:
                sau = suppr_special_char(au).lower()
                ema = sema
                onlypoint = point.search(ema)
                if sau != '' and ema != '' and not onlypoint:
                    if sau in ema:
                        cpt += 1
                        iema = sema.find(sau)
                        lema = list(sema)
                        lema.pop(iema)
                        sema = ''.join(lema)
            if cpt > cpta:
                auth = aut
            cpt = 0
        if affil_in == True:
            affil = affiliation[auth]
        author_email.append([auth, em, affil])
    
    
    if not(emails):
        for d in authors:
            if affil_in == True:
                affil = affiliation[d]
            author_email.append([d, 'N/A', affil])

    return author_email