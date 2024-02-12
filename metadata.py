import fitz

with fitz.open("./ParserPDF/Corpus_test/Torres.pdf") as doc :
    data = doc.metadata
    print(data)
    page = doc.load_page(0)
    print(page.get_textpage().extractXHTML())