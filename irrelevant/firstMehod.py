import irrelevant.directory as directory, fitz

# First method with metadata fields
for pdf in directory.readfiles(directory.input_name) :
    outputName = directory.output_name + pdf + ".txt"
    #print(outputName)
    with fitz.open(pdf) as doc :
        if (doc.metadata.get("title") != "") :
            with open("../" + outputName, 'w+', encoding="utf-8") as output :
                #print(doc.metadata)
                output.write("PDF File: " + pdf + "\n")
                output.write("Title:    " + doc.metadata.get("title") + "\n")
                output.write("Author:   " + doc.metadata.get("author") + "\n")
                output.write("Abstract: ")