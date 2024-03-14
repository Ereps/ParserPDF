import os

output_directory_xml = "xml_output"

def buildXML(pdf) :
    pdf = os.path.basename(pdf)
    output_filename = output_directory_xml + os.sep + pdf
    output_filename = str.replace(output_filename, '.pdf', '.xml')
    print(output_filename)