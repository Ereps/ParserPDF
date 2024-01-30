#! /usr/bin/env python
#coding: utf-8

import fitz

doc = fitz.open("Corpus_test/test_accent.pdf") # open a document

with open("Corpus_result/test_accent.txt", 'w', encoding='utf-8') as fichier_sortie:
    for page in doc: # iterate the document pages
        #text = page.get_text().encode("utf-8")#extract_text().encode('UTF-8') # get plain text (is in UTF-8)
        text = page.get_text()
        print(text)
        fichier_sortie.write(text) # write text of page
        #fichier_sortie.write('\f') # write page delimiter (form feed 0x0C) bytes((12,))
    fichier_sortie.close()