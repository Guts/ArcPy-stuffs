import arcpy

mxd_in = arcpy.mapping.MapDocument(r"D:\A_Ordenar\Julien\LE\octo\mxd\LE_ellipsoides_BN.mxd")
mxd_in.saveACopy(r"D:\A_Ordenar\Julien\LE\octo\mxd\LE_ellipsoides_BN_prov.mxd")

mxd_out = arcpy.mapping.MapDocument(r"D:\A_Ordenar\Julien\LE\octo\mxd\LE_ellipsoides_BN_prov.mxd")
layers = arcpy.mapping.ListLayers(mxd_out)
df = arcpy.mapping.ListDataFrames(mxd_out)[0]


for layer in layers:
    if layer.isGroupLayer and layer.name != u'Capas de base':
        layer.visible = 1
        layer.save
        mxd_out.title = u"Lugares estratégicos de " + unicode(layer.name)
        mxd_out.save()
        arcpy.mapping.ExportToPDF(mxd_out, r"D:\A_Ordenar\Julien\LE\octo\pdf\LE_ellipsoides_BN_" + layer.name + ".pdf")
        arcpy.mapping.RemoveLayer(df, layer)
        mxd_out.save()



ApplySymbologyFromLayer_management(
