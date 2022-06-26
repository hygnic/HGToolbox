# -*- coding: utf-8 -*-
# Create and save a grid for help purpose with step 1

import arcpy as ap
import math

point = ap.Point()
point2 = ap.Point()
array = ap.Array()
lineList = []
#vyska = math.sqrt(7500) + 0.01
vyska = 86.6
size = int(ap.GetParameterAsText(1))
#size = 5.0
if size > 0:
    for X in range(size,100.0,size):
        point.X = X
        point.Y = 0
        point2.X = X/2.0
        point2.Y = (vyska/100.0)*X
        array[0] = point
        array[1] = point2
        polyline = ap.Polyline(array)
        lineList.append(polyline)
        
        point.X = X
        point.Y = 0.0
        point2.X = 50.0 + X/2.0
        point2.Y = (vyska) - (vyska/100.0)*X
        array[0] = point
        array[1] = point2
        polyline = ap.Polyline(array)
        lineList.append(polyline)

        point.X = X/2.0
        point.Y = (vyska/100.0)*X
        point2.X = 100.0 - X/2.0
        point2.Y = (vyska/100.0)*X
        array[0] = point
        array[1] = point2
        polyline = ap.Polyline(array)
        lineList.append(polyline)
        
        print X
    gridName = ap.GetParameterAsText(0)
    workDir = "D:/_temp/pokusne_shp/4/"
    #gridName = workDir + "grid.shp"
    ap.CopyFeatures_management(lineList, gridName)
    lineList.remove
