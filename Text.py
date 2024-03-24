import os, fitz
from extract import authors_emails, block_treatement, title, abstract, introduction, corpus, biblio, conclusion, discu

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
        # Extract and write authors
        abstract_index, abstract_text = abstract.getAbstract(normal_blocks)
        author_email_list = authors_emails.extract(normal_blocks, title_text, abstract_index)
        authors_text = ""
        for author in author_email_list:
            authors_text += author[0] + ", "
        output.write("Authors:\n" + authors_text[:-2] + "\n"*2)
        # Write abstract
        output.write("Abstract:\n" + abstract_text + "\n"*2)
        # Extract INTRO
        output.write("Introduction:\n" + introduction.toString(normal_blocks) + "\n"*2)
        #Extract CORPS
        output.write("Corps:\n" + corpus.toString(normal_blocks) + "\n"*2)
        # TODO: Extract
        #Extract and write conclusion
        conclu_text, conclu_index= conclusion.extract(normal_blocks, doc)
        if len(conclu_text) :
            output.write("Conclusion:\n" + conclu_text + "\n"*2)
        #Extract and write discussion
        discu_text, discu_index = discu.extract(normal_blocks)
        if len(discu_text) :
            output.write("Discussion:\n" + discu_text + "\n"*2)
        #Extract and write references 
        biblio_text, biblio_index= biblio.extract(normal_blocks, doc)
        output.write('References:\n' + biblio_text + "\n"*2)
    print('%s created.' % os.path.basename(output_filename))