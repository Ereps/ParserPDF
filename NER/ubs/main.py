import glob,json,spacy,en_core_web_sm,os,fitz,unicodedata,re,sys

import block_treatement
# Function to read PDF files
def read_files(path,extension):
    current_path = os.getcwd()
    os.chdir(path)
    file_list = []
    for file in glob.glob("*."+extension):
        file_list.append(file)
    os.chdir(current_path)
    return file_list


def load_data(file):
    with open(file,"r") as f:
        data = json.load(f)
    return data

def generate_better_dataset(file):
    data = load_data(file)

    pattern_initial = re.compile(r"([A-Z]\.[ ]*)")
    pattern_and = re.compile(r"(^and[ ]*)")
    new_data = []
    for item in data:
        new_data.append(item)
    #X. name type of author
    for item in data:
        if(re.match(pattern_and,item)):
            for i in item.split("and"):
                if(i != ""):
                    new_data.append(i.replace("and","").strip())
    #split to get only the name
    for item in data:
        if(" " in item):
            for i in item.split(" "):
                if(not re.match(pattern_initial,i) and not re.match(pattern_and,i) and i != "" and len(i) > 2):
                    new_data.append(i)
    for item in data:
        while(pattern_initial.match(item)):
            item = re.sub(pattern_initial,"",item)
    for item in new_data:
        if(pattern_and.match(item)):
            item = re.sub(pattern_and,"",item)
    final_data = []
    titles = ["Mr.","Ms.","Dr.","PhD.","Mrs.","Prof."]
    for item in new_data:
        if item != "":
            final_data.append(item)
            for title in titles:
                titled_data = f"{title} {item}"
                final_data.append(titled_data)
    #ALL CAPS
    for item in new_data:
        item = item.upper()
        if(item != ""):
            final_data.append(item)
            for title in titles:
                titled_data = f"{title} {item}"
                final_data.append(titled_data)
    return final_data
        
def generate_rules(patterns):
    nlp = en_core_web_sm.load()
    ruler = nlp.add_pipe("entity_ruler") #test
    ruler.add_patterns(patterns)
    nlp.to_disk(ner_name)

def create_training_data(file,type):
    data = generate_better_dataset(file)
    patterns = []
    for item in data:
        pattern = {
            "label": type,
            "pattern": item
        }
        patterns.append(pattern)
    return patterns

def get_authors(doc):
    str = doc.metadata.get("author")
    for a in bad_words:
        words = str.split()
        # Filtrer les words qui ne contiennent pas la lettre spécifique
        processed_words = [word for word in words if a not in word]
        # Rejoindre les words filtrés pour former une nouvelle chaîne
        str = ' '.join(processed_words)
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

def test_model(text):
    nlp = spacy.load(ner_name)
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        if ent.label_ == "AUTHOR":
            results.append(ent.text)
    print(results)



pdf_dir = "NER/trainning_data/pdf/"
txt_dir = "NER/trainning_data/text/"
json_name = "NER/tranning_data/name/name.json"
bad_words = ["PhD","@"]

pdf_list = read_files(pdf_dir,"pdf")
txt_list = read_files(txt_dir,"txt")
authors_list = []
ner_name = "NER/ubs/NER_NAME_V1"

#__AUTHORS LIST / PDF TO TEXT
for pdf in pdf_list:
    fname = pdf_dir+pdf
    with fitz.open(fname) as doc:
        #authors_list += get_authors(doc)
        outputFname = txt_dir +pdf + ".txt"
        blocks = []
        """
        with open(outputFname,"w") as file:
            file.write(''.join(authors_list))
        """
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
        
        with open(outputFname,'w', encoding='utf-8') as file:
            for b in blocks:
                file.write(block_treatement.replace_special_char(b[4]))
#__GENERATE NER
"""
patterns = create_training_data("NER/trainning_data/name/better_name.json","AUTHOR")
generate_rules(patterns)
"""
#__GENERATE autor_list json
"""
with open("name/name.json","w") as file:
    file.write(json.dumps(authors_list))

with open(json_name,"w") as file:
    file.write(json.dumps(authors_list))
"""

#nlp = spacy.load(ner_name)

for file_name in txt_list:
    with open(txt_dir+file_name,"r") as file:
        txt = file.read()
        test_model(txt)


