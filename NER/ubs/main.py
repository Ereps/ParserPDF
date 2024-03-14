import glob,json,spacy,en_core_web_sm,os,fitz,unicodedata,re,sys

import block_treatement
# Function to read PDF files
def read_files(path):
    os.chdir(path)
    pdf_list = []
    for file in glob.glob("*.pdf"):
        pdf_list.append(file)
    return pdf_list

def load_data(file):
    with open(file,"r") as f:
        data = json.load(f)
    return data

def generate_better_dataset(file):
    data = load_data(file)
    print(len(data))
    
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
    print(len(new_data))
    titles = ["Mr.","Ms.","Dr.","PhD.","Mrs.","Prof."]
    for item in new_data:
        final_data.append(item)
        for title in titles:
            titled_data = f"{title} {item}"
            final_data.append(titled_data)
    #ALL CAPS
    for item in new_data:
        item = item.upper()
        final_data.append(item)
        for title in titles:
            titled_data = f"{title} {item}"
            final_data.append(titled_data)
    print(len(final_data))
    return final_data
        


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


input_name = "NER/trainning_data/"
output_name = "text/"
json_name = "name/name.json"
bad_words = ["PhD","@"]

pdf_list = read_files(input_name)
authors_list = []

for pdf in pdf_list:
    fname = pdf
    with fitz.open(fname) as doc:
        #authors_list += get_authors(doc)
        outputFname = output_name +fname + ".txt"
        blocks = []
        with open(outputFname,"w") as file:
            file.write(''.join(authors_list))
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
        normal_blocks = block_treatement.blocks_normalization(blocks)
        with open(outputFname,'w', encoding='utf-8') as file:
            for b in normal_blocks:
                file.write(b[4])
        
#TODO PhD,Mr,Ms,

generate_better_dataset(json_name)

with open(json_name,"w") as file:
    file.write(json.dumps(authors_list))


