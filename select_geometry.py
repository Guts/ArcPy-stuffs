import arcpy
import os


output = open(r'C:\Python26\capacitacion\lista_geom_point.txt', 'w')


for fuente, carpeta, archivo in os.walk(r'C:\Python26\capacitacion\SIRAD\BASE_ DATOS_ USO_LIBRE'):

    arcpy.env.workspace = fuente

    for punto in arcpy.ListFeatureClasses('', 'Point'):
        output.write(punto+'\n')
        print punto


output.close()
