import os, fitz
from extract import block_treatement, title, abstract, biblio, authors_emails, conclusion

output_directory_xml = "xml_output"

def buildDir() :
    if not os.path.exists(output_directory_xml) :
        os.mkdir(output_directory_xml)

def buildXML(pdf) :
    pdf_basename = os.path.basename(pdf)
    output_filename = output_directory_xml + os.sep + pdf_basename
    output_filename = str.replace(output_filename, '.pdf', '.xml')
    print('exporting %s...' % pdf_basename)
    with fitz.open(pdf) as doc :
        blocks = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
    normal_blocks = block_treatement.blocks_normalization(blocks)
            
    with open(output_filename, 'w', encoding='utf-8') as output :
        output.write(buildArticle(pdf_basename, doc, 0, normal_blocks))
    print('%s created' % os.path.basename(output_filename))
        
        
def buildArticle(pdf, doc, tabcount, blocks) :
    title_text, title_index = title.extract(blocks, doc)
    abstract_i, abstract_text = abstract.getAbstract(blocks)
    #print(title)
    authors_emails_list = authors_emails.extract(blocks, title_text, abstract_i)
    conclu_text, conclu_i = conclusion.extract(blocks)
    refs, refs_i = biblio.extract(blocks, doc)
    s = '\t' * tabcount + '<article>\n'
    s += buildTitle(pdf, title_text, tabcount+1)
    s += buildAuthors(authors_emails_list, tabcount+1)
    s += buildAbstract(abstract_text, tabcount+1)
    s += buildConclu(conclu_text, tabcount+1)
    s += buildRefs(refs, tabcount+1)
    s += '\t' * tabcount + '</article>\n'
    return s 

def buildTitle(pdf, extract_title, tabcount) :
    s = '\t' * tabcount + '<preambule>' + pdf + '</preambule>\n'
    s += '\t' * tabcount + '<title>' + extract_title + '</title>\n'
    return s

def buildAuthors(authors, tabcount) :
    s = '\t' * tabcount + '<auteurs>\n'
    # TODO: extract authors
    for author in authors :
        s += buildAuthor(author[0], author[1], author[2], tabcount+1)
    s += '\t' * tabcount + '</auteurs>\n'
    return s

def buildAuthor(name, mail, affiliation, tabcount) :
    s = '\t' *tabcount + '<auteur>\n'
    s += '\t' *(tabcount+1) + '<name>' + name + '</name>\n'
    s += '\t' *(tabcount+1) + '<mail>' + mail + '</mail>\n'
    s += '\t' *(tabcount+1) + '<affiliation>' + affiliation + '</affiliation>\n'
    s += '\t' *tabcount + '</auteur>\n'
    return s

def buildAbstract(abstract_string, tabcount) :
    # TODO: extract abstract
    s = '\t' *tabcount + '<abstract>' + abstract_string + '</abstract>\n'
    return s

def buildConclu(conclu_string, tabcount) :
    s = ""
    if len(conclu_string) :
        s = '\t' *tabcount + '<conclusion>' + conclu_string + '<conclusion>\n'
    return s

def buildRefs(refs, tabcount) :
    s = '\t' *tabcount + '<biblio>' + refs + '</biblio>\n'
    return s