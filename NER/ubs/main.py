import glob,json,spacy,en_core_web_sm,os,fitz,unicodedata
# Function to read PDF files
def read_files(path):
    os.chdir(path)
    pdf_list = []
    for file in glob.glob("*.pdf"):
        pdf_list.append(file)
    return pdf_list

def load_data():
    data = []
    txt_list = read_files(input_name)
    print(len(txt_list))
    for txt in txt_list:
        with open(txt) as file:
            data.append(file.read())
    return data

def generate_better_characters(file):
    data = load_data(file)

def get_authors(doc):
    str = doc.metadata.get("author")
    for a in bad_words:
        str.replace(a,"")
    if("Windows" in str):
        str = ""
    authors_list = []
    if str != "": #si le titre apparaît dans la metadata
        if("," in str):
            authors_list= str.split(",")
        else:
            authors_list= str.split(";")
        for i in range (len(authors_list)):
            authors_list[i] = authors_list[i].strip()
        return authors_list
    else:
        return []
def authors_to_json(authors):
    y = json.dumps(authors)


input_name = "NER/trainning_data/"
output_name = "text/"
bad_words = ["and","PhD"]
pdf_list = read_files(input_name)
authors_list = []
for pdf in pdf_list:
    fname = pdf
    with fitz.open(fname) as doc:
        authors_list += get_authors(doc)
        outputFname = output_name +fname + ".txt"
        with open(outputFname,"w") as file:
            file.write(''.join(authors_list))
#TODO PhD,Mr,Ms,
with open("name/name.json","w") as file:
    file.write(json.dumps(authors_list))



with open("name/name.json","r") as file:
    authors_list = json.load(file)
