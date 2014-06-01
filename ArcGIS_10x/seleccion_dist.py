import arcpy
import os


carpeta_busqueda = r'C:\Python26\capacitacion\SIRAD\BASE_ DATOS_ USO_LIBRE'


shape_initial = r'C:\Python26\capacitacion\datos\distritos\distritos.shp'

carpeta_save_select = r"C:\Python26\capacitacion\datos\distritos\\"

campo = 'nombre'

dist = 'SANTA ANITA'

output_folder = r"C:\Python26\capacitacion\datos\output"



cadena_dist = dist.replace(' ', '_').lower()

out_shape = os.path.join(carpeta_save_select, cadena_dist)

# Creo un shape del objeto selecionado y lo guardo
arcpy.Select_analysis(shape_initial, out_shape, '"' + campo + '" = ' +"'"+ dist +"' ")
                      


for fuente, carpeta, archivo in os.walk(carpeta_busqueda):

    arcpy.env.workspace = fuente
    for shape in arcpy.ListFeatureClasses('', 'Point'):
        
        output_name = arcpy.Describe(shape).baseName+ '_' + cadena_dist
    
        arcpy.Intersect_analysis([shape, out_shape + ".shp"],\
                             os.path.join(output_folder, output_name))


        # Si la capa esta vacia, la suprimo
        if int(arcpy.GetCount_management(os.path.join(output_folder, output_name)+'.shp').getOutput(0)) ==0:
            arcpy.Delete_management(os.path.join(output_folder, output_name)+'.shp')
