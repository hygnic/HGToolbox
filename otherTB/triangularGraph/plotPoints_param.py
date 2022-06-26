# -*- coding: utf-8 -*-
# First script for plot input data into triangulat graph.
# Autor: Sukhdorj Ganbaatar (student), s.ganbaatar@seznam.cz
# Department of Geoinformatics, Palacky University in Olomouc
# last update: August 2013

import arcpy as ap
import math
ap.env.overwriteOutput = True
try:
    # parametric input layer, 3 fields from attribute table for calculation and variables
    input = ap.GetParameterAsText(0)
    if ap.Exists(input):
        ap.AddWarning(u" -- Input layer: Ok")
        F1 = ap.GetParameterAsText(1)
        F2 = ap.GetParameterAsText(2)
        F3 = ap.GetParameterAsText(3)
        F1sum = 0
        F2sum = 0
        F3sum = 0
        rowsCount = 0

        # check: fields shouldn't be used more than once
        if F1 == F2 or F2 == F3 or F3 == F1:
            ap.AddError(u" -- Process cannot be completed.")
            ap.AddError(u" -- You have chosen one field many times. Please repeat the operation.")
        else:
            point = ap.Point()      # creat a point instance
            vyska = 86.6            # variable for height of triangle
            pointList = []          # array for hold new points
            checkRows = 0           # variable for check purpose

            # create a cursor object
            rows = ap.SearchCursor(input)
            # FOR loop to iterate rows
            for row in rows:
                # check: values of fields shouldn't be negative
                if row.getValue(F1) < 0 or row.getValue(F2) < 0 or row.getValue(F3) < 0:
                    ap.AddError(u" -- Row data with FID " + str(row.getValue("FID")) + u" contains negative value.")
                    checkRows += 1
                else:
                    # calculate a sum of fileds and check its value
                    sumFields = row.getValue(F1) + row.getValue(F2) + row.getValue(F3)
                    if sumFields == 0:
                        ap.AddError(u" -- Input values for row with FID " + str(row.getValue("FID")) + u" are negative or all are equal zero.")
                        checkRows += 1
                    else:
                        # Calculate a percentage value of three variable phenomenon.
                        # variable sumFields is sums of input value
                        P1_per = row.getValue(F1) * 100.0 / sumFields
                        P2_per = row.getValue(F2) * 100.0 / sumFields
                        P3_per = row.getValue(F3) * 100.0 / sumFields

                        # Auxiliary calculations for further usage
                        F1sum += P1_per
                        F2sum += P2_per
                        F3sum += P3_per
                        rowsCount += 1

                        # Calculate a X, Y coordiantes and save them to the points
                        coordX = P1_per + (P2_per * 0.5)
                        coordY = P2_per * (vyska)/100.0
                        point.X = coordX
                        point.Y = coordY

                        # save a point instance to array
                        bod = ap.Multipoint(point)
                        pointList.append(bod)

            # check a checking variables
            if checkRows == 0:
                ap.AddWarning(u" -- Input variables of three-structured data: Ok")
                pointsName = ap.GetParameterAsText(4)
                ap.CopyFeatures_management(pointList, pointsName)

                # Create auxiliary lines
                createLines = ap.GetParameterAsText(5)
                if createLines != "":
                    F1avg = F1sum/rowsCount
                    F2avg = F2sum/rowsCount
                    F3avg = F3sum/rowsCount
                    Favg = [F2avg,F1avg,F3avg]
                    # ap.AddWarning("F1avg: " + str(F1avg) + ", F2avg: " + str(F2avg) + ", F3avg: " + str(F3avg))

                    # calculate X,Y of lines
                    #linie 1 -> reprezents avg value of 2nd part (F2)
                    Y1 = F2avg*math.sin(math.radians(60))
                    #linie 2 -> reprezents avg value of 1st part (F1)
                    pom1 = F1avg*math.sin(math.radians(60))
                    Y2 = pom1*math.sin(math.radians(30))
                    X2 = pom1*math.sin(math.radians(60))
                    #linie 3 -> reprezents avg value of 3rd part (F3)
                    pom2 = F3avg*math.sin(math.radians(60))
                    Y3 = pom2*math.sin(math.radians(30))
                    X3 = pom2*math.sin(math.radians(60))

                    coordsList = [[[0,Y1],[100,Y1]],
                                  [[X2,0-Y2],[X2+50,0-Y2+vyska]],
                                  [[100-X3,0-Y3],[100-X3-50,0-Y3+vyska]]]
                    # variables to hold points and coordinates of lines
                    #ap.AddWarning(str(coordsList))
                    point2 = ap.Point()
                    array2 = ap.Array()
                    featureList = []
                    # save coordinates to points
                    for linie in coordsList:
                        for bod in linie:
                            point2.X = bod[0]
                            point2.Y = bod[1]
                            array2.add(point2)
                        # create parts of lines and sav them to featurelist
                        polyline = ap.Polyline(array2)
                        array2.removeAll()
                        featureList.append(polyline)
                    # save a line, create a new field to hold a avg value for each line
                    ap.CopyFeatures_management(featureList, createLines)
                    ap.AddField_management(createLines,"TGavg","float")
                    a = 0
                    rows2 = ap.UpdateCursor(createLines)
                    for row2 in rows2:
                        row2.setValue("TGavg",Favg[a])
                        rows2.updateRow(row2)
                        a += 1
                        
                # create a base triangle
                createTriangle = ap.GetParameterAsText(6)
                if createTriangle != "":
                    point3 = ap.Point()
                    array3 = ap.Array()
                    posunY = 0.001
                    coordsList = [[0.0-posunY*2,0.0-posunY],[100.0+posunY*2,0.0-posunY],[50.0,vyska+0.002236]]
                    for XY in coordsList:
                        point3.X = XY[0]
                        point3.Y = XY[1]
                        array3.add(point3)
                    polygon = ap.Polygon(array3)
                    ap.CopyFeatures_management(polygon, createTriangle)

                ap.AddWarning("\n" + u"Summary:")
                ap.AddWarning(u"Successfully created basic layers to construct a triangular graph for input data:")
                ap.AddWarning(str(input) + "\n")
                ap.AddWarning(u"Path to created points:")
                ap.AddWarning(str(pointsName) + "\n")

            else:
                ap.AddWarning("\n" + u"Summary:")
                ap.AddError(u"Impossible to finish task for layer " + str(input) + u" because of invalid input data." + "\n")
    else:
        ap.AddError(u" -- Input layer wasn't found.")
        
except Exception as e:
    ap.AddError("\n" + u" Unexpected errors:")
    ap.AddError(" - " + e.message)
    ap.GetMessages(2)