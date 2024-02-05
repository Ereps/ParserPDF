import subprocess

# Chemin vers le fichier PDF d'entrée
input_pdf_path = "Corpus_test/Boudin-Torres-2006.pdf"

# Chemin vers le fichier texte de sortie
output_text_path = "Corpus_result/Boudin-Torres-2006_pdf2txt.txt"

# Appel de pdf2txt en utilisant subprocess
subprocess.run(["pdf2txt", "-o", output_text_path, "-A", input_pdf_path])

print(f"Texte extrait avec succès et enregistré dans {output_text_path}")
