import re
import nltk
from nltk.tag.stanford import StanfordNERTagger
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from extract.block_treatement import *
from nameparser import HumanName
#TODO pip install nameparser
#TODO python -m nltk.downloader popular


PATH_TO_JAR='../NER/stanford-corenlp-french.jar'
PATH_TO_MODEL = '../NER/classifiers/english.all.3class.distsim.crf.ser.gz'
def get_human_names(text):
    #print(text)
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                print(chunk.label(), ' '.join(c[0] for c in chunk))
    tagger = StanfordNERTagger(model_filename=PATH_TO_MODEL,path_to_jar=PATH_TO_JAR, encoding='utf-8')
    words = nltk.word_tokenize(text) 
    tagged = tagger.tag(words)
    #print(tagged)


def extract(blocks,title,abstract_index):
    index = 0
    name_list = []
    text = ""
    for x in range(len(blocks)):
        if title in blocks[x][4]:
            index = x+1
            break
    for i in range(index, abstract_index[0], 1):
        text += blocks[i][4]
    name_list.append(get_human_names(text))

#TODO toress moreno faux positif avec matière condensée
def extract2(blocks, title, abstract_index):
    email = []
    author = []
    emails = []
    authors = []
    author_email=[]
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
    #abstract_index[0] == premier abstract block
    for i in range(index, abstract_index[0], 1):
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

    # for aut in authors:
    #     auth = suppr_special_char(aut).lower()
    #     cpte = 0
    #     cpt = 0
    #     ema = ''
    #     for em in emails:
    #         for e in em:
    #             if e == '@' or e=='q' or e=='Q':
    #                 break
    #             elif e in auth:
    #                 cpt += 1
    #         if cpt > cpte:
    #             ema = em
    #     author_email.append([aut, ema])
    
    for em in emails:
        ema = ''
        for c in em:
            if c == '@' or c == 'Q':
                break
            else:
                ema += c
        #print(ema)
        cpta = 0
        cpt = 0
        auth=''
        for aut in authors:
            for au in aut:
                if suppr_special_char(au).lower() in ema:
                    cpt += 1
                    #print(suppr_special_char(au).lower())
            if cpt > cpta:
                auth = aut
               # print(auth)
                #print(cpt)
            cpt = 0
        author_email.append([auth, em])

    #print(author_email)

    #print(authors)
    #print(emails)
    return authors, emails