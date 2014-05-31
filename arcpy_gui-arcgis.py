#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     06/01/2012
# Copyright:   (c) Utilisateur 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from arcpy import *
import os

fuente = GetParameterAsText(0)
nombre = GetParameterAsText(1)

#########

output = open(nombre, 'w')

for source, carpeta, archivo in os.walk(fuente):
    arcpy.env.workspace = source
    for punto in arcpy.ListFeatureClasses('', 'Point'):
        output.write(punto+'\n')
        AddMessage(punto)
output.close()