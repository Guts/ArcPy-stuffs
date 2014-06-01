# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : GDB Geom Fixer
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
                  SearchCursor, RepairGeometry_management
from os import sep, path
from datetime import date


## Variables
gdb = 'D:\Datos\SIRAD_2012.gdb'
enviro.workspace = gdb

table = gdb + r"\Informe_GeometriaCapas_20121025"
feats = []
prevFc = ""

for row in SearchCursor(table):
    fc = row.getValue("CLASS")
    if fc != prevFc:
        prevFc = fc
        feats.append(fc)

for fc in feats:
    print "Processing " + fc
    RepairGeometry_management(fc)
