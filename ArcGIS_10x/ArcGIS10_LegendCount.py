#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        Metadator
# Purpose:     Create dynamically metadata files about shapefiles according to
#              profiles created by user before through the form.
# Author:      Julien M. et Pierre V.
#
# Created:     19/12/2011
# Updated:     19/03/2012
# Changelog :
#
#-------------------------------------------------------------------------------


###################################
##### Import des librairies #######
###################################

from arcpy import mapping
from arcpy import GetCount_management

from Tkinter import Tk as root
from tkFileDialog import askopenfile

###################################
####### Programme principal #######
###################################


cible = askopenfile(parent=root(), mode='r')
mxd = mapping.MapDocument(cible.name)



layers = mapping.ListLayers(mxd)
for lay in layers:
    if lay.isFeatureLayer:
        lay.name = lay.name + " (" + str(GetCount_management(lay)) + ")"

mxd.save()
del mxd, cible

root.destroy()