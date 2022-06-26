##################################################
#Inspired by: School of Engineering, University of Zambia (UNZA)
#Survey Community - Zambia (Arc1950)
#Developer: ebenezer.odoi@gmail.com  +16145943273
##################################################


import os
import sys
import arcpy

arcpy.env.overwriteOutput = True
# import pythonaddins



#######User Selection 1
poly_lyr = arcpy.GetParameterAsText(0)
# poly_lyr = r"C:\Users\EB\Desktop\polygons\Export_OutputPro.shp"

#######User Selection 2
# num_out_polys = 10
num_out_polys = int(arcpy.GetParameterAsText(1))
#map units (eg meters) and the difference in area between the largest and the smallest polygons
#0.005 - 0.02%; 0.01 - 0.03%; 0.05 - 0.1%; 0.1 - 0.3%;
step_value = 1

#######User Selection 3
# orientation = 'NS' #'WE' / 'NS'
orientation = arcpy.GetParameterAsText(2)

if orientation != 'NS' or orientation != 'WE':
    orientation == 'NS'

# number of splits
splits = [round(float(100)/float(num_out_polys), 2)] * num_out_polys

#spatial reference of the output fc will be of the polygon layer
sr = arcpy.SpatialReference(arcpy.Describe(poly_lyr).spatialReference.factoryCode)

#source polygon fields
fields = [f.name for f in arcpy.ListFields(poly_lyr) if not f.required]

if int(arcpy.GetCount_management(poly_lyr).getOutput(0)) != 1:
    arcpy.AddMessage('Need to have exactly one feature selected', 'Error')
    sys.exit(0)

#get polygon geometry and extent property
with arcpy.da.SearchCursor(poly_lyr, fields + ["SHAPE@"]) as cur:
    for row in cur:
        attributes = list(row[:-1])
        polygon = row[-1]
        extent = polygon.extent

#orient lines either North-South (up-down) or West-East (left to right)
if orientation == 'NS':
    x_max = extent.XMax + step_value
    x_min = extent.XMin + step_value
    y_max = extent.YMax
    y_min = extent.YMin

if orientation == 'WE':
    x_max = extent.XMax
    x_min = extent.XMin
    y_max = extent.YMax - step_value
    y_min = extent.YMin

cut_poly = polygon
# name of output shapefile
outputshape_name = arcpy.GetParameterAsText(3)
#output feature class create/clean
# arcpy.env.scratchGDB
mem_path = os.path.join(arcpy.Describe(poly_lyr).path, str(outputshape_name)+".shp")
if arcpy.Exists(mem_path):
    arcpy.Delete_management(mem_path)
mem = arcpy.CopyFeatures_management(poly_lyr, mem_path)
arcpy.DeleteFeatures_management(mem)

lines = []

with arcpy.da.InsertCursor(mem, fields + ["SHAPE@"]) as icur:
    for i in splits[:-1]: #need to get all but the last item
        tolerance = 0
        while tolerance < i:
            pnt_arr = arcpy.Array()
            if orientation == 'NS':
                #construct North-South oriented line
                pnt_arr.add(arcpy.Point(x_min, y_max))
                pnt_arr.add(arcpy.Point(x_min, y_min))

            if orientation == 'WE':
                #construct West-East oriented line
                pnt_arr.add(arcpy.Point(x_min, y_max))
                pnt_arr.add(arcpy.Point(x_max, y_max))

            line = arcpy.Polyline(pnt_arr, sr)
            lines.append(line)

            #cut polygon and get split-parts
            cut_list = cut_poly.cut(line)
            if orientation == 'NS':
                tolerance = 100 * cut_list[1].area / polygon.area
                x_min += step_value

            if orientation == 'WE':
                tolerance = 100 * cut_list[0].area / polygon.area
                y_max -= step_value

        # part 0 is on the right side and part 1 is on the left side of the cut
        if orientation == 'NS':
            cut_poly = cut_list[0]
            icur.insertRow(attributes + [cut_list[1]])

        if orientation == 'WE':
            cut_poly = cut_list[1]
            icur.insertRow(attributes + [cut_list[0]])

    #insert last cut remainder
    if orientation == 'NS':
        icur.insertRow(attributes + [cut_list[0]])

    if orientation == 'WE':
        icur.insertRow(attributes + [cut_list[1]])

#for illustration purposes only
arcpy.CopyFeatures_management(lines, 'in_memory/lines')

#evaluation of the areas error
done_polys = [f[0] for f in arcpy.da.SearchCursor(mem_path, 'SHAPE@AREA')]

#the % of the smallest and the largest areas
# arcpy.AddMessage("{} Precision error".format(round(100 - 100 * (min(done_polys) / max(done_polys)), 2)))
arcpy.AddWarning("OutPut Path is :"+mem_path)
