# -*- coding: cp1252 -*-
# import des modules usuels
import os, sys, glob, string, shutil, arcgisscripting

# cr�ation de l'objet de g�otraitement
gp = arcgisscripting.create(9.3)

# D�finition environnement de travail
gp.workspace = "D:\\A ordenar\\Julien\\tratamientos"

# Chargement outils
# gp.AddToolbox("C:/Archivos de programa/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")
# gp.AddToolbox("C:/Archivos de programa/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")

# D�crire un objet
desc = gp.Describe("D:\\A ordenar\\Julien\\test\\areas_expansion.shp")

print desc.DataType
print desc.CatalogPath

