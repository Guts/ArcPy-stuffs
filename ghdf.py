# ---------------------------------------------------------------------------
# ghdf.py
# Created on: lun. sept. 05 2011 11:45:43 
#   (generated by ArcGIS/ModelBuilder)
# Usage: ghdf <LE_SoloEsenciales_Sup0> 
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create()

# Load required toolboxes...
gp.AddToolbox("C:/Program Files (x86)/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")

# Script arguments...
LE_SoloEsenciales_Sup0 = sys.argv[1]
if LE_SoloEsenciales_Sup0 == '#':
 LE_SoloEsenciales_Sup0 = "LE_SoloEsenciales_Sup0" # provide a default value if unspecified

# Local variables...
agE = "LE_SoloEsenciales_Sup0"
ag_code = "LE_SoloEsenciales_Sup0"
EcodeAg = "LE_SoloEsenciales_Sup0"
alE = "LE_SoloEsenciales_Sup0"
al_code = "LE_SoloEsenciales_Sup0"
EcodeAl = "LE_SoloEsenciales_Sup0"
LE_SoloEsenciales_Sup0__3_ = "LE_SoloEsenciales_Sup0"
LE_SoloEsenciales_Sup0__2_ = "LE_SoloEsenciales_Sup0"
EnE = "LE_SoloEsenciales_Sup0"
al_code__2_ = "LE_SoloEsenciales_Sup0"
EcodeAl__2_ = "LE_SoloEsenciales_Sup0"
LE_SoloEsenciales_Sup0__4_ = "LE_SoloEsenciales_Sup0"





# Process: agE = 1...
gp.SelectLayerByAttribute_management(LE_SoloEsenciales_Sup0, "NEW_SELECTION", "\"AGUA_E\" =1")
gp.AddField_management(agE, "ag_code", "TEXT", "", "", "1", "", "NON_NULLABLE", "NON_REQUIRED", "")
gp.CalculateField_management(ag_code, "ag_code", "\"A\"", "VB", "")

# Process: alE = 1...
gp.SelectLayerByAttribute_management(LE_SoloEsenciales_Sup0, "NEW_SELECTION", "\"ALIMEN_E\" =1")
gp.AddField_management(alE, "al_code", "TEXT", "", "", "1", "", "NON_NULLABLE", "NON_REQUIRED", "")
gp.CalculateField_management(al_code, "al_code", "\"L\"", "VB", "")

# Process: EnE = 1...
gp.SelectLayerByAttribute_management(LE_SoloEsenciales_Sup0, "NEW_SELECTION", "\"ENERG_E\" =1")
gp.AddField_management(LE_SoloEsenciales_Sup0__4_, "en_code", "TEXT", "", "", "1", "", "NON_NULLABLE", "NON_REQUIRED", "")
gp.CalculateField_management(al_code__2_, "en_code", "\"E\"", "VB", "")



# Process: Select Layer By Attribute...
gp.SelectLayerByAttribute_management(LE_SoloEsenciales_Sup0, "CLEAR_SELECTION", "")
gp.CalculateField_management(LE_SoloEsenciales_Sup0__2_, "CODE_types", "[ag_code] + [al_code]", "VB", "")

