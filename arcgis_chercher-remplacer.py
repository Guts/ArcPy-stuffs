# -*- coding: cp1252 -*-
# import des modules usuels
import os, sys, glob, string, shutil, arcgisscripting

# cr�ation de l'objet de g�otraitement
gp = arcgisscripting.create(9.3)

# D�finition environnement de travail
gp.workspace = "D:\\A ordenar\\Julien\\tratamientos"



replace([attribut],"aremplacer","remplacement")
