import os, fitz
from extract import block_treatement, title, abstract, biblio, authors_emails, conclusion, discu, introduction, corpus

output_directory_xml = "xml_output"

def buildDir() :
    if not os.path.exists(output_directory_xml) :
        os.mkdir(output_directory_xml)

def buildXML(pdf, toBegin: int, page_id: int) :
    pdf_basename = os.path.basename(pdf)
    output_filename = output_directory_xml + os.sep + pdf_basename
    output_filename = str.replace(output_filename, '.pdf', '.xml')
    print('exporting %s...' % pdf_basename)
    with fitz.open(pdf) as doc :
        blocks = []
        for page_num in range(page_id, len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
    normal_blocks = block_treatement.blocks_normalization(blocks)
            
    with open(output_filename, 'w', encoding='utf-8') as output :
        output.write(buildArticle(pdf_basename, doc, 0, normal_blocks, toBegin))
    print('%s created' % os.path.basename(output_filename))
        
        
def buildArticle(pdf, doc: fitz.open, tabcount: int, blocks: list, toBegin: int) :
    #print(blocks[0])
    title_text, title_i = title.extract(blocks, doc, toBegin)
    #print("Title I : ", title_i)
    abstract_i, abstract_text = abstract.getAbstract(blocks)
    #print(title)
    #authors_emails_list = authors_emails.extract(blocks, title_i, abstract_i)
    intro_text = introduction.toString(blocks)
    corps_text = corpus.toString(blocks)
    conclu_text, conclu_i = conclusion.extract(blocks, doc)
    discu_text, discu_i = discu.extract(blocks)
    refs, refs_i = biblio.extract(blocks, doc)
    s = '\t' * tabcount + '<article>\n'
    s += buildTitle(pdf, title_text, tabcount+1)
    #s += buildAuthors(authors_emails_list, tabcount+1)
    s += buildAbstract(abstract_text, tabcount+1)
    s += buildIntro(intro_text, tabcount+1)
    s += buildCorps(corps_text, tabcount+1)
    s += buildDiscu(discu_text, tabcount+1)
    s += buildConclu(conclu_text, tabcount+1)
    s += buildRefs(refs, tabcount+1)
    s += '\t' * tabcount + '</article>\n'
    return s 

def buildTitle(pdf, extract_title, tabcount) :
    s = '\t' * tabcount + '<preamble>' + pdf + '</preamble>\n'
    s += '\t' * tabcount + '<titre>' + extract_title + '</titre>\n'
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
    s += '\t' *(tabcount+1) + '<nom>' + name + '</nom>\n'
    s += '\t' *(tabcount+1) + '<mail>' + mail + '</mail>\n'
    s += '\t' *(tabcount+1) + '<affiliation>' + affiliation + '</affiliation>\n'
    s += '\t' *tabcount + '</auteur>\n'
    return s

def buildAbstract(abstract_string, tabcount) :
    # TODO: extract abstract
    s = '\t' *tabcount + '<abstract>' + abstract_string + '</abstract>\n'
    return s

def buildIntro(intro_string, tabcount) :
    s = '\t' *tabcount + '<introduction>' + intro_string + '</introduction>\n'
    return s

def buildCorps(corps_string, tabcount) :
    s = '\t' *tabcount + '<body>' + corps_string + '</body>\n'
    return s

def buildConclu(conclu_string, tabcount) :
    s = ""
    if len(conclu_string) :
        s = '\t' *tabcount + '<conclusion>' + conclu_string + '</conclusion>\n'
    else :
        s = '\t' *tabcount + '<conclusion>' + 'N/A' + '</conclusion>\n'
    return s

def buildDiscu(discu_string, tabcount) :
    s = ""
    if len(discu_string) :
        s = '\t' *tabcount + '<discussion>' + discu_string + '</discussion>\n'
    else :
        s = '\t' *tabcount + '<discussion>' + 'N/A' + '</discussion>\n'
    return s

def buildRefs(refs, tabcount) :
    s = '\t' *tabcount + '<biblio>' + refs + '</biblio>\n'
    return s