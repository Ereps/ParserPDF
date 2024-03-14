import re
from extract.block_treatement import *

"""
il n'y a pas forcément de conclusion, sa position dans le doc change selon la présence ou non d'appendix, acknowledgments, discussion (peut être avant ou après)
le titre est toujours composé de "conclusion" ou "c onclusion"
il y a un cas où en remontant le texte à l'envers, le premier "conclusion" trouvé n'est pas celui du titre de la partie conclusion : jing-cutepaste. dans ce cas le "conclusion" est dans la partie Acknowledgments
note : faut ignorer appendix, future work, acknowledgment pour la sortie
"""