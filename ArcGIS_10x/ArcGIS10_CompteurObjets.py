# -*- coding: UTF-8 -*-
#!/usr/bin/env python

### Import des modules
from Tkinter import Tk                      # interface graphique
from tkMessageBox import showinfo           # fenêtre d'information
from tkFileDialog import askdirectory       # fenêtre de choix de dossier

from arcpy import env, GetCount_management, ListFeatureClasses  # outils arcpy

## variables du GUI
root = Tk()         # création instance fenêtre
root.withdraw()     # empêcher la fenêtre de "fond"

## variables script globales
env.workspace = askdirectory()  # prompt graphique du workspace
enr = 0    # compteur d'enregistrements

### Programme principal
for f in ListFeatureClasses():
    """ boucle sur les features présents dans le workspace """
    result = int(GetCount_management(f).getOutput(0))   # comptage d'objet avec récupération du résultat d'ArcGIS
    enr = enr + result    # incrémentation compteur

## appel de la fenêtre
# paramètres fenêtre
showinfo(title = "Fin et résultat du traitement",    # titre de la fenêtre
         message = "Le traitement est terminé : "
                   + str(objs) + " enregistrements trouvés parmi "
                   + str(len(ListFeatureClasses())) + " objets"
                   + ". Consulter la fenêtre résultat d'ArcGIS pour plus de détails.") # message affiché dans la fenêtre