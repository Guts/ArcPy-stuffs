#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     17/11/2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from arcpy import env
from arcpy import CheckOutExtension as check_licence
from arcpy import CalculateField_management as calc_champ
from arcpy import MakeFeatureLayer_management as trans_lyr
from arcpy import SelectLayerByAttribute_management as sel_attr

from arcpy.sa import PointStatistics as stats_pts
from arcpy.sa import NbrCircle

from sys import exit as EXIT



# Environnement de travail
env.workspace = "D:\\Julien\\tratamientos\\mask"

# Masque
env.mask = "D:\\Julien\\tratamientos\\mask\\t_t328.ovr"

# Variables
pts = "D:\\Julien\\tratamientos\\mask\\New_Manzana_poblacion_punto.shp"
lyr = trans_lyr(pts)
chp = "3tipos_5cl"

cell = 15
neighb = NbrCircle(600, "CELL")

# Vérification des licences nécessaires
check_licence("Spatial")

res_stat_pts = stats_pts(pts, chp, cell, neighb, "MAJORITY")
res_stat_pts.save("D:\\Julien\\tratamientos\\mask\\statpts_output")