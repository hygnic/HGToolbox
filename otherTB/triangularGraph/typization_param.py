# -*- coding: utf-8 -*-
# Second script (the last one) to typization data based on zones of triangulat grapf and point layer from first script
# Autor: Sukhdorj Ganbaatar (student), s.ganbaatar@seznam.cz
# Department of Geoinformatics, Palacky University in Olomouc
# last update: January 2014 (fix English messages)

import arcpy as ap
import math
ap.AddWarning("-- Start: Data classification")

# Input variables
zoneNames =  []
i = 0
z = ap.GetParameterAsText(0)
fieldName = ap.GetParameterAsText(1)

# Read a field value of each row and save it to array
rows = ap.SearchCursor(z,"","",fieldName)
for row in rows:
    zoneNames.append(row.getValue(fieldName))
    i += 1
ap.AddWarning(" -- Categories of triangulat point graph were successfully loaded.")
##ap.AddWarning(zoneNames)

# Copy a geometry of points and zones
p = ap.GetParameterAsText(2)
#pointsFeature = ap.CopyFeatures_management(p,ap.Geometry())
points = ap.CopyFeatures_management(p,ap.Geometry())
zones = ap.CopyFeatures_management(z,ap.Geometry())
pointZona = []      # variable for hold a categories for points
zonesErr = 0        # check variables
pointsErr = 0
unknownErr = 0
pointNo = 0

# Loop to iterate points and zones and compare their position
#for points in pointsFeature:
for point in points:
    j = 0
    count = 0
    for zona in zones:
        # Test if point is within zone
        if point.within(zona) == True:
            count += 1      # Counts a amount of polygons that contains 1 point (1 point should lay on 1 polygon)
            # Add a category of polygon layer (containing zones) to array
            pointZona.append(zoneNames[j])
        j += 1
    ##ap.AddWarning(" -- count: " + str(count))
    if count == 1:
        print " -- Input points and polygons: OK"
    elif count == 0:
        ap.AddError(" -- Point with FID " +str(pointNo)+ " is out of any zone.")
        pointsErr += 1
    elif count > 1:
        ap.AddError(" -- Point with FID " +str(pointNo)+ " is within 2 or more zones.")
        zonesErr += 1
    else:
        ap.AddError(" -- Unknown error: point with FID " +str(pointNo))
        unknownErr += 1
    pointNo += 1

##ap.AddWarning("zonesErr = "+str(zonesErr))
##ap.AddWarning("pointsErr = "+str(pointsErr))
##ap.AddWarning("unknownErr = "+str(unknownErr))

# Check conditions
if unknownErr == 0:
    if zonesErr == 0 and pointsErr == 0:
        m = 0
        # Create a new field in attribute table
        new_field = ap.GetParameterAsText(3)
        valNewField = ap.ValidateFieldName(new_field)
        ap.AddField_management(p,valNewField,"text")
        # Create a cursor object to edit input data for point layer
        rows = ap.UpdateCursor(p)
        for row in rows:
            row.setValue(valNewField, str(pointZona[m]))
            rows.updateRow(row)
            m += 1
        del row, rows

        input = ap.GetParameterAsText(4)
        n = 0
        # Create a new field in attribute table
        ap.AddField_management(input,valNewField,"text")
        # Create a cursor object to edit input data for input data (original input data)
        rows = ap.UpdateCursor(input)
        for row in rows:
            row.setValue(valNewField, str(pointZona[n]))
            rows.updateRow(row)
            n += 1
        if n == pointNo:
            ap.AddWarning("\nSummary:")
            ap.AddWarning(" -- Classification was successful.")
            ap.AddWarning(" -- "+ str(pointNo) + " rows were classified.")
            ap.AddWarning(" -- Update was done for layer: " + str(input))
        else:
            ap.AddError(" -- Classification was successful but it seems that output classes were written to wrong layer.")
            ap.AddWarning(" -- Please check your layer and classes. If it's necesary repeat proces.")
            ap.AddWarning(" -- You have choosen this layer to write classes: " + str(input))
    else:
        ap.AddWarning("\nSummary:")
        ap.AddError(" -- Tool couldn't finish the task because of invalid input data.")
        ap.AddError(" -- Causes of this error are writted above.")
else:
    ap.AddError(" -- Unknown error")
    ap.AddError(" -- Please try to reset tool or save your work and reset ArcGIS.")

ap.AddWarning("-- End: Data classification")
