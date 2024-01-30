from PyPDF2 import PdfReader
 
#create file object variable
#opening method will be rb
reader=PdfReader("Corpus_test/Boudin-Torres-2006.pdf",'rb')
numPages = len(reader.pages)
file1=open("Corpus_result/Boudin-Torres-2006.txt","a")
for i in range(0,numPages):
    page = reader.pages[i]
    text = page.extract_text()
    file1.writelines(text)