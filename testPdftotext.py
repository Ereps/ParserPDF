import subprocess

# Chemin vers le fichier PDF d'entrée
input_pdf_path = "Corpus_test/Boudin-Torres-2006.pdf"

# Chemin vers le fichier texte de sortie
output_text_path = "Corpus_result/Boudin-Torres-2006_pdftotext.txt"

# Appel de pdftotext en utilisant subprocess
#subprocess.run(["pdftotext", "-layout", input_pdf_path, output_text_path])
subprocess.run(["pdftotext", input_pdf_path, output_text_path])

print(f"Texte extrait avec succès et enregistré dans {output_text_path}")
