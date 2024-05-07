import json
import spacy
import re
import making_dataset
def test_model(text):
    """
    Test the NER model on the given text and extract entities labeled as "AUTHOR".

    Args:
        text (str): The input text to test the NER model on.

    Returns:
        list: A list of extracted entities labeled as "AUTHOR".
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            author = process_author(ent.text)
            if(author !=""):
                results.append(author)
    print(results)
    return results

def replace_special_char(text):
    text = text.strip()
    continus_word = re.compile(r'-( )*\n')
    text = re.sub(continus_word,"",text)
    text = text.replace('\n', ' ')
    text = text.replace('- ', '')
    text = text.replace('`A', 'À')
    text = text.replace('^A', 'Â')
    text = text.replace('"A', 'Ä')
    text = text.replace('`E', 'È')
    text = text.replace('¨E', 'Ë')
    text = text.replace('^E', 'Ê')
    text = text.replace('´E', 'É')
    text = text.replace('¨I', 'Ï')
    text = text.replace('^I', 'Î')
    text = text.replace('`I', 'Ì')
    text = text.replace('`U', 'Ù')
    text = text.replace('¨U', 'Ü')
    text = text.replace('`¨U', 'Ǜ')
    text = text.replace('^U', 'Û')
    text = text.replace('`O', 'Ò')
    text = text.replace('¨O', 'Ö')
    text = text.replace('^O', 'Ô')
    text = text.replace('`Y', 'Ỳ')
    text = text.replace('¨Y', 'Ÿ')
    text = text.replace('^Y', 'Ŷ')
    text = text.replace('^Z', 'Ẑ')
    text = text.replace('^S', 'Ŝ')
    text = text.replace('^G', 'Ĝ')
    text = text.replace('^H', 'Ĥ')
    text = text.replace('¨H', 'Ḧ')
    text = text.replace('^J', 'Ĵ')
    text = text.replace('¨W', 'Ẅ')
    text = text.replace('^W', 'Ŵ')
    text = text.replace('`W', 'Ẁ')
    text = text.replace('^C', 'Ĉ')
    text = text.replace('¨X', 'Ẍ')
    text = text.replace('`N', 'Ǹ')
    text = text.replace('´e', 'é')
    text = text.replace('`e', 'è')
    text = text.replace('^e', 'ê')
    text = text.replace('"e', 'ë')
    text = text.replace('¨a', 'ä')
    text = text.replace('^a', 'â')
    text = text.replace('`a', 'à')
    text = text.replace('´a', 'á')
    text = text.replace('°a', 'å')
    text = text.replace('"ı', 'ï')
    text = text.replace('ˆı', 'î')
    text = text.replace('`ı', 'ì')
    text = text.replace('`u', 'ù')
    text = text.replace('`¨u', 'ǜ')
    text = text.replace('"u', 'ü')
    text = text.replace('^u', 'û')
    text = text.replace('`o', 'ò')
    text = text.replace('"o', 'ö')
    text = text.replace('^o', 'ô')
    text = text.replace('`y', 'ỳ')
    text = text.replace('"y', 'ÿ')
    text = text.replace('^y', 'ŷ')
    text = text.replace('´y', 'ý')
    text = text.replace('^z', 'ẑ')
    text = text.replace('^s', 'ŝ')
    text = text.replace('^g', 'ĝ')
    text = text.replace('^h', 'ĥ')
    text = text.replace('"h', 'ḧ')
    text = text.replace('^j', 'ĵ')
    text = text.replace('`w', 'ẁ')
    text = text.replace('^w', 'ŵ')
    text = text.replace('"w', 'ẅ')
    text = text.replace('^c', 'ĉ')
    text = text.replace('c¸', 'ç')
    text = text.replace('"t', 'ẗ')
    text = text.replace('"x', 'ẍ')
    text = text.replace('`n', 'ǹ')

    return text

def process_author(text :str) ->str:
    noNum = r'[0-9]+'
    final_text = re.sub(noNum,"",text)
    final_text = replace_special_char(final_text)
    accent = "éèêëäâàáåïîìùǜüûòöôỳÿŷýẑŝĝĥḧĵẁŵẅĉçẗẍǹÉÈÊËÄÂÀÁÅÏÎÌÙǛÜÛÒÖÔỲŸŶÝẐŜĜĤḦĴẀŴẄĈÇT̈ẌǸ"
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
    nlp = spacy.load("en_core_web_sm")
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
    #nlp = spacy.load("xx_sent_ud_sm")

    for file_name in txt_list:
        with open(txt_dir + file_name, "r") as file:
            print(file_name)
            txt = file.read()
            result += test_model(txt)

            
    with open("/NER/ubs/result/result.json", "w+") as file:
        file.json.dumps(result)

