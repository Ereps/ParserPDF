import re

from extract.block_treatement import *


def extract(blocks, index, abstract_index) -> list:
    email = []
    author = []
    emails = []
    authors = []
    author_email=[]
    affiliation = {}
    a = []
    e = []
    date = []
    no_no_in = False
    affil_in = False
    affil = ''
    cpt = 1
    author_pattern = re.compile(r'[A-Z][a-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]*)?(?: +[A-Zinhugdlaeiouàáâäçèéêëìíîïñòóôöùúûüýÿﬁ.]{0,5})?(?:[.]*)? [A-Z][A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ]+(?:-[A-Za-zàáâäçèéêëìíîïñòóôöùúûüýÿﬁ-]*)?')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    semi_mail_pattern = re.compile(r'[@qQ][A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    date_pattern = re.compile(r'(?:(?:[January]{7})|(?:[February]{8})|(?:[March]{5})|(?:[April]{5})|(?:[May]{3})|(?:[June]{4})|(?:[July]{4})|(?:[August]{6})|(?:[September]{9})|(?:[October]{7})|(?:[November]{8})|(?:[December]{8}))[ ]*[0-9]{1,4}[, ]*[0-9]{1,4}')
    no_no_words = ['Université', 'Bretagne', 'Nord', 'Sud', 'Est ', 'Ouest', 'University', 'Universitat', 'North', 'South', 'West', 'Laboratoire', 'Laboratory', 'LIMSI-CNRS', 'Univ', 'Rennes', 'Informatique', 'Centre', 'Center', 'Europe', 'Google', 'Inc', 'Fondamentale', 'Marseille', 'France', 'Aix-Marseille', 'Vannes', 'Canada', 'Montréal', 'Polytechnique', 'Mexico', 'Avignon', 'Instituto', 'Ingeniería', 'Institute', 'Institue', 'Linguistics', 'Spain', 'Mexique', 'Espagne', 'Québec', 'Pays', 'Vaucluse', 'Meinajaries', 'Département', 'Centre-ville', 'New York', 'Department', 'Computer', 'Science', 'Columbia', 'Technologies', 'Carnegie', 'Mountain', 'View', 'Ecole', 'Centre', 'Ville', 'Cedex', 'Scalable', 'Approach', 'Sentence', 'Scoring', 'Multi', 'Document', 'Multi-Document', 'Update', 'Word', 'Representations', 'Vector', 'Space', 'System', 'Demonstrations', 'Processing', 'Tool', 'Matière', 'Condensée', 'Compiled', 'April', 'November', 'January', 'February', 'March', 'May', 'June', 'July', 'August', 'September', 'December', 'Institut', 'Universitari', 'Lingüística', 'Aplicada', 'Barcelona', 'La', 'Rambla', 'Xerox', 'Research', 'Artiﬁcial', 'Arificial', 'Intelligence', 'Domaine', 'Chesnay']
    
    # Trouver l'indice du bloc contenant le titre
    if index == 0:
        index += 1
    
    for i in range(index, abstract_index, 1):

        if 'Abstract' in blocks[i][4] or 'abstract' in blocks[i][4] or 'ABSTRACT' in blocks[i][4]:
            i += 1
            if abstract_index <= i:
                break
        block_text = replace_special_char(blocks[i][4]) #remplace tous les accents
        author_match = author_pattern.search(block_text) #cherche les auteurs
        email_match = email_pattern.search(block_text) #cherche les mails
        semi_mail_match = semi_mail_pattern.search(block_text) #cherche les fins de mails
        date_match = date_pattern.search(block_text)#cherche des dates

        if(date_match):
            date.append(date_pattern.findall(block_text))
            for d in date[0]:
                block_text = block_text.replace(d, '')#supprime les dates

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

        for t in authors:
            block_text = block_text.replace(t, '') #supprime les auteurs du texte

        if(email_match): #si on a trouvé des mails
            email.append(email_pattern.findall(block_text)) #ajoute dans la liste de mails
            emails = [element for sous_liste in email for element in sous_liste]
            if len(email) == 1: #si on a qu'un seul mail
                email_match = email_pattern.search(block_text)
                email_index = email_match.start()
                if block_text[email_index-1] == ',' or block_text[email_index-2] == ',': #si jamais on trouve une virgule avant le mail
                    email_match = email_pattern.search(block_text)
                    email_index = email_match.start()
                    semi_mail_match = semi_mail_pattern.search(block_text)
                    end_email = semi_mail_pattern.findall(block_text)
                    e = block_text.split(',') #on sépare le texte grâce aux virgules
                    for m in e: #on boucle sur les éléments du texte séparé
                        if m != email[0][0] and ' ' not in m and m != '': #si l'élément est différent du mail
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
        
        #cherche les chaînes de textes pas intéressantes
        notWanted = re.compile(r'^[a-z∗†]{0,1}[,]* *[&♮♭⇑*†]+ *(?:[,]{0,1}[ ]*[a-z†∗]{0,1})*| *[0-9,sthrnd]{3}(?:[(][A-Za-z]{0,1}[)])?(?: +|$)|[&♮♭⇑*† ]{2}|[ ,]+$|^(?:[and]{3}[ &♮♭⇑*∗†]*)+')
        nw = notWanted.findall(block_text)

        #remplace les chaînes de texte non voulu par un espace
        for n in nw:
            block_text = block_text.replace(n, ' ')
        
        #cherche les bouts de textes pas intéressant pour les affiliations
        notAffiliation = re.compile(r'^ *[,*.]+ *[,*. ]*|^ *[and]{3} *[ &♮♭⇑*∗†]*| +$')
        isAffiliation = notAffiliation.fullmatch(block_text)
        
        #si au moins une partie du texte est intéressant
        if isAffiliation == None:
            #enlève les espaces à la fin du texte
            if block_text.endswith(' '):
                block_text = block_text.removesuffix(' ')
            #enlève les espaces au début du texte
            if block_text.startswith(' '):
                block_text = block_text.removeprefix(' ')

            ajout = False
            same = True
            
            #associe une affiliation ou un bout d'affiliation aux auteurs
            for r in authors:
                #si l'auteur n'a pas encore d'affiliation, on lui ajoute le texte
                if r not in affiliation:
                    affiliation[r] = block_text.strip()
                    affil_in = True
                    ajout = True

            #si le texte n'a pas encore été ajouté et qu'il y a des auteurs
            if ajout == False and cpt < 4 and len(authors) > 0 :
                affiliations = {}
                v = affiliation[authors[0]]
                
                #vérifie que tous les auteurs on les mêmes affiliations
                for key, value in affiliation.items():
                    if value != v:
                        same = False
                
                #si les affiliations sont les mêmes ppour tous les auteurs, on ajoute le texte à tous les auteurs
                if same and block_text != '':
                    for key, value in affiliation.items():
                        affiliations[key] = value + ' ' + block_text.strip()
                    affiliation = affiliations
                    cpt += 1
                #si les affiliations sont différentes en fonction des auteurs, on ajoute le texte au dernier auteur
                elif not same and block_text != '':
                    k = [*affiliation.keys()]
                    v = [*affiliation.values()]
                    affiliation[k[-1]] = v[-1] + ' ' + block_text.strip()    

    #regroupe les auteurs, emails et affiliations par couple si il y a des emails
    for em in emails:
        ema = ''

        #ne garde que la première partie du mail
        for c in em:
            if c == '@' or c == 'Q':
                break
            else:
                ema += c
        
        cpta = [0,'']
        cpt = 0
        auth=''
        sema = ema
        point = re.compile('^[.]+$')
        
        #cherche quel auteur à le plus de similarité avec le début du mail
        for aut in authors:

            #regarde pour chaque lettre si il est contenu dans le mail
            for au in aut:
                sau = suppr_special_char(au).lower()
                ema = sema
                onlypoint = point.fullmatch(ema)
                if sau != '' and ema != '' and not onlypoint:
                    if sau in ema:
                        cpt += 1
                        iema = sema.find(sau)
                        lema = list(sema)
                        lema.pop(iema)
                        sema = ''.join(lema)
            
            #si le nombre de lettres contenu dans le mail est suppérieur à l'ancien auteur, on garde le nouvel auteur et son compteur en référence
            if cpt > cpta[0]:
                cpta[0] = cpt
                cpta[1] = aut
            cpt = 0
        
        auth = cpta[1]
        authors.remove(auth)
        
        if affil_in == True:
            affil = affiliation[auth]
        
        author_email.append([auth, em, affil.strip()])
    
    #regroupe les auteurs, emails et affiliations si il n'y a pas d'emails
    if not(emails):
        
        for d in authors:
            if affil_in == True:
                affil = affiliation[d]
            author_email.append([d, 'N/A', affil.strip()])

    #si aucun auteur n'est trouvé
    for aut in author_email:
        if aut[-1] == '':
            aut[-1] = 'N/A'

    return author_email