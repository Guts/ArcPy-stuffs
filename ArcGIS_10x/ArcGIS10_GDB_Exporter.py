# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name : GDB Exporter
# Purpose : Export all features classes from a GDB rebuilding the same
#           organization of the database
# Authors : Julien Moura
# Contact : julien.moura@ird.fr
# Python : 2.6.5
# Encoding: utf-8
# Created : 07/11/2012
# Updated : 08/11/2012
#-------------------------------------------------------------------------------

## Import modules

from arcpy import env as enviro
from arcpy import ListDatasets, ListFeatureClasses, FeatureClassToShapefile_conversion,
                  AddMessage, AddWarning, GetParameterAsText
from os import mkdir, chdir, getcwd

## Variables environnement ArcGIS
gdb = 'D:\Datos\SIRAD_2012.gdb'
enviro.workspace = gdb

env.overwriteOutput = True
enviro.maintainSpatialIndex = True

AddMessage("Workspace eligido: %s" % enviro.workspace)

## Variables environnement Windows
cible = r'C:\Documents and Settings\Utilisateur\Mes documents\GIS DataBase'
AddMessage("Carpeta de destino eligida: %s" % cible)

chdir(cible)
try:
    mkdir('SIRAD')
except:
    
cible = cible + '\SIRAD'
chdir(cible)


for dataset in ListDatasets("","featuredataset"):
    AddMessage("Dataset: %s" % dataset)
    print dataset
    mkdir(dataset)
    enviro.workspace = gdb + '\\' + dataset
    if len(ListFeatureClasses()) > 0:
        FeatureClassToShapefile_conversion(ListFeatureClasses(), cible + '\\' + dataset)
        AddMessage(u'Capas de información de %s exportadas' % dataset)
        print u'Capas de información de %s exportadas' % dataset
    else:
        AddWarning(u'Ninguna capa de información encontrada en %s' % dataset)
        print u'Ninguna capa de información encontrada en %s' % dataset

