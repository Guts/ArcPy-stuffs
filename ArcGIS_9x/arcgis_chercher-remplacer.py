# -*- coding: cp1252 -*-
# import des modules usuels
import os, sys, glob, string, shutil, arcgisscripting

# création de l'objet de géotraitement
gp = arcgisscripting.create(9.3)

# Définition environnement de travail
gp.workspace = "D:\\A ordenar\\Julien\\tratamientos"



replace([attribut],"aremplacer","remplacement")
