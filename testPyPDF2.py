#! /usr/bin/env python
#coding: utf-8

from PyPDF2 import PdfReader
import codecs


#create file object variable
#opening method will be rb
reader=PdfReader("Corpus_test/Boudin-Torres-2006.pdf",strict=False)
numPages = len(reader.pages)
file1=codecs.open("Corpus_result/Boudin-Torres-2006.txt","a",encoding='utf-8')

text = ""


for current_page in reader.pages:
    text += current_page.extract_text()
file1.write(text)