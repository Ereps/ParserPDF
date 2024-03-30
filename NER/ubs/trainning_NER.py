import json,spacy,en_core_web_sm,re,random
import making_dataset

def test_model(text):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            results.append(ent.text)
    print(results)
    return results

def generate_rules(patterns):
    nlp = en_core_web_sm.load()
    ruler = nlp.add_pipe("entity_ruler") #test
    ruler.add_patterns(patterns)
    nlp.to_disk(ner_name)



result = []
ner_name = "NER/ubs/NER_NAME_V1"
txt_dir = "NER/trainning_data/text/"
txt_list = making_dataset.read_files(txt_dir,"txt")




#__GENERATE NER
"""
patterns = making_dataset.create_training_data("NER/trainning_data/name/better_name.json","AUTHOR")
generate_rules(patterns)
"""


from bs4 import BeautifulSoup
 
 
# Reading the data inside the xml
# file to a variable under the name 
# data
"""
with open('NER/trainning_data/xml/dblp.xml', 'r') as f:
    data = f.read()
    print(data)
"""
#__TEST NER
nlp = en_core_web_sm.load()


for file_name in txt_list:
    with open(txt_dir+file_name,"r") as file:
        print(file_name)
        txt = file.read()
        result += test_model(txt)
        
with open("/NER/ubs/result/result.json","w+") as file:
    file.json.dumps(result)

