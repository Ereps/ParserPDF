#! /usr/bin/env python
#coding: utf-8

import pathlib, glob, os

output_name = "output/"
input_name="Corpus_test/"

#Lire les fichiers pdf
def readfiles(path):
    os.chdir(path)
    pdfs = []
    for file in glob.glob("*.pdf"):
       pdfs.append(file)
    return pdfs

#Remove directory
def rmdir(directory):
    directory = pathlib.Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

if(pathlib.Path(output_name).exists()):
    rmdir(output_name)
pathlib.Path(output_name).mkdir(parents=True, exist_ok=True)