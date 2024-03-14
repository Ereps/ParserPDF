import os

output_directory_txt = "txt_output"

def buildTEXT(pdf) :
    pdf = os.path.basename(pdf)
    output_filename = output_directory_txt + os.sep + pdf
    output_filename = str.replace(output_filename, '.pdf', '.txt')
    print(output_filename)