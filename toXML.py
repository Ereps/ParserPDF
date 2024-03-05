import glob
import os
import pathlib
import fitz
import extract.abstract
import extract.authors
import extract.biblio
import extract.title

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
def buildXML(pdf, doc, blocks) :
    output_filename = output_directory_xml + os.sep + pdf + '.xml'
    print(output_filename)
    with open(output_filename, 'w', encoding='utf-8') as output :
        output.write(buildArticle(pdf, doc, 0, blocks))

# calls TITLE, AUTHORS, ABSTRACT
def buildArticle(pdf, doc, tabcount, blocks) :
    title = extract.title.extract_title(blocks, doc)
    abstract, abstract_i = extract.abstract.abstract.extract_abstract(blocks)
    #print(title)
    authors_list, mails = extract.authors.extract_authors(blocks, title, abstract_i)
    refs, refs_i = extract.biblio.extract_biblio(blocks, title)
    s = '\t' * tabcount + '<article>\n'
    s += buildTitle(title, tabcount+1)
    s += buildAuthors(authors_list, tabcount+1)
    s += buildAbstract(abstract, tabcount+1)
    s += buildRefs(refs, tabcount+1)
    s += '\t' * tabcount + '</article>\n'
    return s 

def buildTitle(extract_title, tabcount) :
    s = '\t' * tabcount + '<preambule>' + pdf + '</preambule>\n'
    s += '\t' * tabcount + '<title>' + extract_title + '</title>\n'
    return s

def buildAuthors(authors, tabcount) :
    s = '\t' * tabcount + '<auteurs>\n'
    # TODO: extract authors
    for author in authors :
        s += buildAuthor(author, '', tabcount+1)
    s += '\t' * tabcount + '</auteurs>\n'
    return s

def buildAuthor(name, mail, tabcount) :
    s = '\t' *tabcount + '<auteur>\n'
    s += '\t' *(tabcount+1) + '<name>' + name + '</name>\n'
    s += '\t' *(tabcount+1) + '<mail>' + mail + '</mail>\n'
    s += '\t' *tabcount + '</auteur>\n'
    return s

def buildAbstract(abstract_string, tabcount) :
    # TODO: extract abstract
    s = '\t' *tabcount + '<abstract>' + abstract_string + '</abstract>\n'
    return s

def buildRefs(refs, tabcount) :
    s = '\t' *tabcount + '<biblio>' + refs + '</biblio>\n'
    return s

pdf_list = read_files(input_directory)

# make the directory
if pathlib.Path(output_directory_xml).exists() :
    rmdir(output_directory_xml)
pathlib.Path(output_directory_xml).mkdir(parents=True, exist_ok=True)

for pdf in pdf_list :
    with fitz.open(pdf) as doc :
        page = doc.load_page(0)
        blocks=  [] #list of all the text blocks
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text_blocks()
        buildXML(pdf, doc, blocks)

        '''
        page = doc.load_page(0)
        blocks = page.get_textpage().extractDICT().get('blocks')
        font_size = blocks[0]['lines'][0]['spans'][0]['size']
        for text_instance in blocks :
            
            for line in text_instance['lines'] :
                for span in line['spans'] :
                    font_sizes = span['size']
        '''