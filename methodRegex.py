import re, directory, fitz
import spacy

nlp = spacy.load("en_core_web_sm")
import re, irrelevant.directory as directory, fitz

# Method with Regex
for pdf in directory.readfiles(directory.input_name) :
    outputName = directory.output_name + pdf + ".txt"
    #print(outputName)
    with fitz.open(pdf) as doc :
        print(pdf)
        page = doc.load_page(0)
        blocks = page.get_textpage().extractBLOCKS()
        text = page.get_textpage().extractText()
        for block in blocks :
            name_regex = re.compile(r'[A-Z][a-z]*\.?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+$', re.MULTILINE)
            name_regex = re.compile(r'[A-Z][a-z]*\.? +(?:[A-Z][a-z]*\.? *)*[A-Z][a-z]+$', re.MULTILINE)
            print(name_regex.findall(block[4]))
            #print(re.findall(r"^Abstract", block[4]))


# j'ai essayé d'utiliser une librairie pour les noms mais ça fonctionne qu'à moitié...
def extract_person_names(text):
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return persons

person_names = extract_person_names(text)
print("Noms propres de personnes trouvés dans le PDF :")
for name in person_names:
    print(name)