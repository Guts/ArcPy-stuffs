#-------------------------------------------------------------------------------
# Name:        Make a buffer within a mask
# Purpose:
#
# Author:      Julien M.
#
# Created:     17/11/2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from arcpy import env
from arcpy import CheckOutExtension as check_licence
from arcpy import MakeFeatureLayer_management as trans_lyr
from arcpy import Buffer_analysis as buff

from sys import exit as EXIT



# Environnement de travail
env.workspace = "D:\\Julien\\tratamientos\\mask"
# Masque
env.mask = "D:\\Julien\\tratamientos\\mask\\Zona_urbana.shp"

# Variables
pts = "D:\\Julien\\tratamientos\\mask\\New_Manzana_poblacion_punto.shp"
lyr = trans_lyr(pts)
sortie = "D:\\Julien\\tratamientos\\mask\\poblacion_punto_buffoutput2.shp"

# Exec
buff(lyr, sortie, 600, "FULL", "ROUND")
buff(lyr, sortie, 600, "FULL", "ROUND")

EXIT()