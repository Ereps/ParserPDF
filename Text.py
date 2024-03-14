import os, fitz
from extract import block_treatement, title, abstract, biblio

output_directory_txt = "txt_output"

def buildDir() :
    if not os.path.exists(output_directory_txt) :
        os.mkdir(output_directory_txt)

def buildTEXT(pdf) :
    pdf_basename = os.path.basename(pdf)
    output_filename = output_directory_txt + os.sep + pdf_basename
    output_filename = str.replace(output_filename, '.pdf', '.txt')
    print('exporting %s...' % pdf_basename)
    with fitz.open(pdf) as doc :
        blocks = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
    normal_blocks = block_treatement.blocks_normalization(blocks)
    
    with open(output_filename, 'w', encoding='utf-8') as output :
        output.write("PDF File:\n" + pdf_basename + "\n"*2)
        # Extract and write title
        title_text, title_index = title.extract(normal_blocks, doc)
        output.write("Title:\n" + title_text + "\n"*2)
        # TODO: Extract and write authors
        # Extract and write abstract
        abstract_text, abstract_index = abstract.extract(normal_blocks)
        output.write("Abstract:\n" + abstract_text + "\n"*2)
        #Extract and write references 
        biblio_text, biblio_index= biblio.extract(normal_blocks, title_text)
        output.write('References:\n' + biblio_text + "\n"*2)
    print('%s created.' % os.path.basename(output_filename))