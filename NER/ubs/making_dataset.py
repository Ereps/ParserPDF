import html
import glob,json,spacy,en_core_web_sm,os,fitz,unicodedata,re,sys
import xml.sax



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
    bad_words = ["PhD","@"," and ", "Windows","Anonymous","mat","Six"]

    pattern_initial = re.compile(r"([A-Z]\.[ ]*)")
    pattern_and = re.compile(r"(^and[ ]*)")
    new_data = []
    #remove names with bad words
    for item in data:
        for j in bad_words :
            if(j in item):
                data.remove(item)
                break
    
    #add all the good names
    for item in data:
        new_data.append(item)
        

    """
    for item in data:
        if(re.match(pattern_and,item)):
            for i in item.split("and"):
                if(i != ""):
                    new_data.append(i.replace("and","").strip())
    """
    #split to get only the name
    for item in data:
        if(" " in item):
            for i in item.split(" "):
                if( len(item.split(" ")) < 3):
                    if(not re.match(pattern_initial,i) and not re.match(pattern_and,i) and i != "" and len(i) > 2):
                        new_data.append(i)
    for item in data:
        while(pattern_initial.match(item)):
            item = re.sub(pattern_initial,"",item)
    """
    for item in new_data:
        if(pattern_and.match(item)):
            item = re.sub(pattern_and,"",item)
    """
    final_data = []
    for item in new_data:
        if(item != ""):
            final_data.append(item)
    """
    titles = ["Mr.","Ms.","Dr.","PhD.","Mrs.","Prof."]
    for item in new_data:
        if item != "":
            final_data.append(item)
            for title in titles:
                titled_data = f"{title} {item}"
                final_data.append(titled_data)
    """
    #ALL CAPS
    for item in new_data:
        item = item.upper()
        if(item != ""):
            final_data.append(item)
            """
            for title in titles:
                titled_data = f"{title} {item}"
                final_data.append(titled_data)
            """
    print(len(final_data))
    return final_data
        


def get_authors(doc):
    str = doc.metadata.get("author")
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




pdf_dir = "NER/trainning_data/pdf/"
txt_dir = "NER/trainning_data/text/"
json_name = "NER/trainning_data/name/name.json"
json_better_name = "NER/trainning_data/name/better_name.json"


pdf_list = read_files(pdf_dir,"pdf")
txt_list = read_files(txt_dir,"txt")
authors_list = []

#__AUTHORS LIST / PDF TO TEXT
for pdf in pdf_list:
    fname = pdf_dir+pdf
    with fitz.open(fname) as doc:
        authors_list += get_authors(doc)
        outputFname = txt_dir +pdf + ".txt"
        blocks = []
        text = ""
        """
        with open(outputFname,"w") as file:
            file.write(''.join(authors_list))
        """
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks += page.get_text("blocks")
            #text += blocks[page_num][4] + " "

        with open(outputFname,'w', encoding='utf-8') as file:
            #file.write(block_treatement.replace_special_char(text))
            for b in blocks:
                file.write(block_treatement.replace_special_char(b[4]))

#DBLP ONLY AUTHOR

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self, save_path):
        self.current_tag = ""
        self.author = ""
        self.save_path = save_path

    def startElement(self, tag, attributes):
        self.current_tag = tag

    def endElement(self, tag):
        if self.current_tag == "author":
            with open(self.save_path, 'a') as f:
                f.write(f'{json.dumps(self.author)}\n')
        self.current_tag = ""

    def characters(self, content):
        if self.current_tag == "author":
            self.author = content

def parse_author_from_dblp(dblp_path, save_path):
    parser = xml.sax.make_parser()
    parser.setContentHandler(DBLPHandler(save_path))
    parser.parse(dblp_path)
parse_author_from_dblp("NER/trainning_data/xml/dblp.xml","NER/trainning_data/dblp_author.json")

#__GENERATE autor_list json
"""
with open(json_name,"w") as file:
    file.write(json.dumps(authors_list))

with open(json_better_name,"w") as file:
    file.write(json.dumps(generate_better_dataset(json_name)))
"""




