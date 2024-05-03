import json
import spacy
import en_core_web_sm
import re
import random
import making_dataset

def test_model(text):
    """
    Test the NER model on the given text and extract entities labeled as "AUTHOR".

    Args:
        text (str): The input text to test the NER model on.

    Returns:
        list: A list of extracted entities labeled as "AUTHOR".
    """
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            author = process_author(ent.text)
            if(author !=""):
                results.append(author)
    print(results)
    return results

def process_author(text :str) ->str:
    noNum = r'[0-9]+'
    final_text = re.sub(noNum,"",text)
    accent = "éèêëäâàáåïîìùǜüûòöôỳÿŷýẑŝĝĥḧĵẁŵẅĉçẗẍǹ"
    #Remove non letter character
    final_text = re.sub(r'[^a-zA-Z\s' +accent+r']', '', final_text)
    #Remove space
    final_text = final_text.strip()
    #Remove if the text is 2 or less character
    if(len(final_text) < 3):
        final_text = ""
    #Remove if the first character isn't in uppercase
    elif(final_text[0].islower()):
        final_text = ""
    
    return final_text

def generate_rules(file):
    """
    Generate rules for the NER model based on the patterns defined in the given file.

    Args:
        file (str): The path to the file containing the patterns for generating rules.
    Returns:
        None
    """
    nlp = en_core_web_sm.load()
    ruler = nlp.add_pipe("entity_ruler")
    i = 0
    with open(file, "r") as file:
        for line in file:
            i += 1
            print(i)
            pattern = [json.loads(line)]
            ruler.add_patterns(pattern)
    nlp.to_disk(ner_name)

result = []
ner_name = "NER/ubs/NER_NAME_V2"
txt_dir = "NER/trainning_data/text/"
txt_list = making_dataset.read_files(txt_dir, "txt")
json_trainning_dataset_V2 = "NER/trainning_data/name/trainning_dataset_V2.json"
json_trainning_dataset_V3 = "NER/trainning_data/name/trainning_dataset_V3.json"

if __name__ == "__main__":
    #__GENERATE NER



    #__TEST NER
    nlp = en_core_web_sm.load()

    for file_name in txt_list:
        with open(txt_dir + file_name, "r") as file:
            print(file_name)
            txt = file.read()
            result += test_model(txt)

            
    with open("/NER/ubs/result/result.json", "w+") as file:
        file.json.dumps(result)

