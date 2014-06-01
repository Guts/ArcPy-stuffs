from arcpy import *

cible = r"D:\A_Ordenar\Julien\LE\octo\shp"
env.workspace = r"D:\A_Ordenar\Julien\LE\octo\shp"

for shp in ListFeatureClasses('*ellipsoides*'):
    chps = []
    for c in ListFields(shp):
        chps.append(c.name)
    if "activado" not in chps:
        AddField_management(shp, "activado", "SHORT", 1)
    if "tipo" not in chps:
        AddField_management(shp, "tipo", "TEXT", 150)

del shp, chps, cible