import re
import linecache as lc

def extract_abstract(text):
    # Regex pattern to find "Introduction" or "INTRODUCTION"
    intro_pattern = re.compile(r'Introduction|INTRODUCTION')

    # Regex pattern to find "Abstract" or "ABSTRACT"
    abstract_pattern = re.compile(r'Abstract|ABSTRACT')

    this_pattern = re.compile(r'In this article|This article')

    # Search for the introduction keyword
    intro_match = intro_pattern.search(text)

    if intro_match:
        # Get the index of the introduction keyword
        intro_index = intro_match.start()

        # Initialize abstract string
        abs_rev = ""
        
        # Counter for the number of paragraphs found
        paragraph_count = 0 # TODO USELESS

        # Search backwards from the introduction keyword to find the abstract
        abstract_match = abstract_pattern.search(text[:intro_index])
        this_match = this_pattern.search(text[:intro_index])

        # If abstract keyword found, extract abstract
        if abstract_match:
            abstract_index = abstract_match.start()

            # Extract abstract in reverse order
            abs_rev = text[abstract_index:intro_index]

            #remplacer ce qu'il faut pour de la mise en forme
            abs_rev = abs_rev.replace('\n', ' ')
            abs_rev = abs_rev.replace('Abstract', ' ')
            abs_rev = abs_rev.replace('Abstract.', ' ')
            abs_rev = abs_rev.replace('1', ' ')
            abs_rev = abs_rev.replace('I.', ' ')
            abs_rev = abs_rev.replace('1.', ' ')
            abs_rev = abs_rev.replace('- ', '')

            return abs_rev.strip()  # Return abstract string stripped of leading/trailing whitespaces
        else:
    # Abstract keyword not found, search backward for two paragraphs
            this_index = this_match.start()

            abs_rev = text[this_index:intro_index]

            # Replace newline characters with spaces
            abs_rev = abs_rev.replace('\n', ' ')
            abs_rev = abs_rev.replace('Abstract', ' ')
            abs_rev = abs_rev.replace('Abstract.', ' ')
            abs_rev = abs_rev.replace('1', ' ')
            abs_rev = abs_rev.replace('I.', ' ')
            abs_rev = abs_rev.replace('1.', ' ')
            abs_rev = abs_rev.replace('- ', '')

            return abs_rev.strip()  # Return abstract string stripped of leading/trailing whitespaces


    # If either introduction keyword is not found, return empty string
    return ""

def extract_title(doc):
    title = ""
    if doc.metadata.get("title") != "":
        title = doc.metadata.get('title')
    title = title.replace('\n', ' ')
    
    return title

def extract_authors(outputFname, title):
    author_string = ""
    with open(outputFname, 'r', encoding='utf-8') as file:
        # Initialize variables
        line = file.readline()
        # Search for the first occurrence of the three first words of the title
        target_words = title.split()[:3]
        # Initialize a buffer to store lines for searching the target words
        buffer = []
        while line:
            buffer.append(line)
            if len(buffer) > len(target_words):
                buffer.pop(0)
            if all(word in ' '.join(buffer) for word in target_words):
                break
            line = file.readline()
        
        # Move to the next paragraph
        while line.strip():  # Skip empty lines
            line = file.readline()

        # Read and store characters until a keyword is found
        while line:
            author_string += line
            line = file.readline()
            if re.search(r'Abstract|In this article|This article', line):
                #TODO Comme titre, trouver les cinqs premiers mots
                break
    

    # Clean author string
    author_string = author_string.strip()
    author_string = author_string.replace('\n', ' ')
    author_string = author_string.replace('- ', '')
    author_string = author_string.replace('´e', 'é')
    author_string = author_string.replace('`e', 'è')
    author_string = author_string.replace('´a', 'à')

    # Return the extracted author information
    return author_string

# TODO: extract email from authors
def extract_email() :
    print()