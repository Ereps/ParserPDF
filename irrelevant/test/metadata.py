import fitz

with fitz.open("./Corpus_test/Nasr.pdf") as doc :
    data = doc.metadata
    print(data)
    page = doc.load_page(0)
    print(page.get_textpage().extractXHTML())


# Write in txt UTF-8
"""
with open("metadata.txt", 'w', encoding="utf-8") as file :
    file.write("ç")
"""