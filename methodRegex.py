import re, directory, fitz

# Method with Regex
for pdf in directory.readfiles(directory.input_name) :
    outputName = directory.output_name + pdf + ".txt"
    #print(outputName)
    with fitz.open(pdf) as doc :
        print(pdf)
        page = doc.load_page(0)
        blocks = page.get_textpage().extractBLOCKS()
        for block in blocks :
            name_regex = re.compile(r'[A-Z][a-z]*\.?\s+(?:[A-Z][a-z]*\.?\s*)?[A-Z][a-z]+$', re.MULTILINE)
            name_regex = re.compile(r'[A-Z][a-z]*\.? +(?:[A-Z][a-z]*\.? *)*[A-Z][a-z]+$', re.MULTILINE)
            print(name_regex.findall(block[4]))
            #print(re.findall(r"^Abstract", block[4]))