import extractBis, fitz

with fitz.open('Corpus_test/Boudin-Torres-2006.pdf') as doc :
    extractBis.extractTitle(doc)