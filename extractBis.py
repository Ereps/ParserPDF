import os, fitz

def extractTitle(doc : fitz.open) :
    print(doc.metadata.get('title'))