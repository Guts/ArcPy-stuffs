# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : GDB Geom Checker
# Purpose : Runs various operations on the SIRAD database : listing, check geometry
# Authors : Julien Moura
# Contact : julien.moura@ird.fr
# Python : 2.7.x
# Encoding: utf-8
# Created : 25/10/2012
# Updated : 25/10/2012
# Source : http://help.arcgis.com/fr/arcgisdesktop/10.0/help/index.html#//001700000034000000
#-------------------------------------------------------------------------------

## Import modules

from arcpy import env as enviro
from arcpy import ListDatasets, ListFeatureClasses, \
                  CheckGeometry_management, GetCount_management
from os import sep
from datetime import date

## Variables

hoy = hoy = str(date.today()).replace('-', '')  # date du jour
gdb = 'D:\Datos\SIRAD_2012.gdb'
enviro.workspace = gdb
CheckOut = gdb + sep + "Informe_GeometriaCapas_" + hoy # table des résultats

feats = []  # liste des couches de la gdb
 
for dataset in ListDatasets("","featuredataset"):
    feats += ListFeatureClasses("*", "", dataset)
          
# List all standalone feature classes
#fcs = ListFeatureClasses()
     
print u"Se esta chequeando la geometría de %i capas" % len(feats)
CheckGeometry_management(feats, CheckOut)

print (str(GetCount_management(CheckOut)) + u" problemas de geometría han sido encontrados.")
print (u"Ver " + CheckOut + u" para los detalles")
