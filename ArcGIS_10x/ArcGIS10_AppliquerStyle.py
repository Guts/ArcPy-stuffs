import arcpy

mxd_in = arcpy.mapping.MapDocument(r"D:\A_Ordenar\Julien\LE\octo\mxd\LE_elementos_BN.mxd")
layers = arcpy.mapping.ListLayers(mxd_in)

style_apoyo = r"D:\A_Ordenar\Julien\LE\lyr\PresenciaRecursosApoyo_NB.lyr"
style_esenciales = r"D:\A_Ordenar\Julien\LE\lyr\PresenciaRecursosEsenciales_NB.lyr"

for layer in layers:
    if "esenciales" in layer.name:
        arcpy.ApplySymbologyFromLayer_management(layer, style_esenciales)
        layer.save
    elif "apoyo" in layer.name:
        arcpy.ApplySymbologyFromLayer_management(layer, style_apoyo)
        layer.save

mxd_in.save()

del mxd_in, layers
