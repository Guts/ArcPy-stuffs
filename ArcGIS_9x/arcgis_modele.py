# -*- coding: cp1252 -*-
#--------------------------------
# Nom:        modele.py
# Objectif:
# Auteur:    Julien Moura
# Crée le    23/06/2011
# Copyright:  (c) IRD
# ArcGIS Version:  9.3
# Python Version:  2.5
#--------------------------------


# import des modules usuels
import os, arcgisscripting

# création de l'objet de géotraitement
gp = arcgisscripting.create(9.3)

# Définition environnement de travail
gp.workspace = "D:\\A ordenar\\Julien\\tratamientos"

