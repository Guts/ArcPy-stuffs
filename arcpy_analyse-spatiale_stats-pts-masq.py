#-------------------------------------------------------------------------------
# Name:        Pauline - script analyse par points
# Purpose:     Statistiques par points à l'intérieur d'un masque.
#
# Author:      Julien Moura
#
# Created:     17/11/2011
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from arcpy import env
from arcpy import CheckOutExtension as check_licence
from arcpy.sa import PointStatistics as stats_pts
from arcpy.sa import NbrCircle



# Environnement de travail
env.workspace = u"D:\\A_Ordenar\\Julien\\tratamientos\\mask"

# Masque
env.mask = "Zona_urbana.shp"

# Variables
pts = u"D:\\A_Ordenar\\Julien\\tratamientos\\mask\\New_Manzana_poblacion_punto.shp"
chp = u"3tipos_5cl"

cell = 15
neighb = NbrCircle(600, u"CELL")

# Vérification des licences nécessaires
check_licence(u"Spatial")

res_stat_pts = stats_pts(pts, chp, cell, neighb, "MAJORITY")
res_stat_pts.save(u"D:\\A_Ordenar\\Julien\\tratamientos\\mask\\testoutput")