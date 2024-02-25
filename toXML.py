import glob
import os
import pathlib
import fitz
import extract

output_directory_xml = "xml_output"
input_directory = "Corpus_test"
##
def read_files(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
        pdfs.append(file)
    return pdfs

def rmdir(directory):
    directory = pathlib.Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()
##

# calls ARTICLE
def buildXML(pdf, doc) :
    output_filename = output_directory_xml + os.sep + pdf + '.xml'
    print(output_filename)
    with open(output_filename, 'w', encoding='utf-8') as output :
        output.write(buildArticle(pdf, doc, 0))

# calls TITLE, AUTHORS, ABSTRACT
def buildArticle(pdf, doc, tabcount) :
    s = '\t' * tabcount + '<article>\n'
    s += buildTitle(pdf, doc, tabcount+1)
    s += buildAuthors(doc, tabcount+1)
    s += buildAbstract(doc, tabcount+1)
    s += '\t' * tabcount + '</article>\n'
    return s 

def buildTitle(pdf, doc, tabcount) :
    s = '\t' * tabcount + '<preambule>' + pdf + '</preambule>\n'
    s += '\t' * tabcount + '<title>' + extract.extract_title(doc) + '</title>\n'
    return s

def buildAuthors(doc, tabcount) :
    s = '\t' * tabcount + '<auteurs>\n'
    # TODO: extract authors
    
    s += '\t' * tabcount + '</auteurs>\n'
    return s

def buildAbstract(doc, tabcount) :
    # TODO: extract abstract
    s = '\t' *tabcount + '<abstract>' + '</abstract>\n'
    return s

pdf_list = read_files(input_directory)

# make the directory
if pathlib.Path(output_directory_xml).exists() :
    rmdir(output_directory_xml)
pathlib.Path(output_directory_xml).mkdir(parents=True, exist_ok=True)

for pdf in pdf_list :
    with fitz.open(pdf) as doc :
        page = doc.load_page(0)
        buildXML(pdf, doc)

        '''
        page = doc.load_page(0)
        blocks = page.get_textpage().extractDICT().get('blocks')
        font_size = blocks[0]['lines'][0]['spans'][0]['size']
        for text_instance in blocks :
            
            for line in text_instance['lines'] :
                for span in line['spans'] :
                    font_sizes = span['size']
        '''