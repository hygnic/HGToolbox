# -*- coding: iso8859-1 -*-
#-------------------------------------------------------------------------------
# Name: Spider.py
# Purpose: Create line from Fclass center (origin) to Fclass border (destination) using ID field.
#
# Author: fpr - support esri France
#
# Created:     08/27/2009
# Updated:     01/07/2013 for ArcGIS for Desktop 10.0 and 10.1
#              - Add 2 new fields: ID_CENTER and ID_BORDER to store input OBJECTID in output feature class.
#              => now you can make a join !
#              - you can use shapefile or feature class in Geodatabase as input or output  
#             
# Copyright:   (c) esri France
# ArcGIS Version:   10.0 and 10.1 SP1
# Python Version:   2.6
#-------------------------------------------------------------------------------
import os
import sys
import arcpy

def CreateLine(firstPoint, endPoint):
    """Create line object using first point and end point

    INPUTS:
    first point, end point

    OUTPUT:
    line object
    """

    #Create line
    line = arcpy.Array()
    line.add(firstPoint)
    line.add(endPoint)
    
    return line

def CreateLineUsingPoint(firstPoint, arcTan, lineLength):
    import math
    """ Return line from start point, angle and length

    INPUTS:
    first point, end point, length

    OUTPUT:
    line object
    """

    #Create line
    ligne = arcpy.Array()
    ligne.add(firstPoint)
    
    #Calculate end point
    endPoint = arcpy.Point()
    endPoint.X = firstPoint.X - math.sin(arcTan)* lineLength
    endPoint.Y = firstPoint.Y - math.cos(arcTan)* lineLength

    ligne.add(endPoint)
    
    return ligne

def DistanceBetween2Points(firstPoint, endPoint):
    import math
    """Calculate arc tan between two points.

    INPUTS:
    first point, end point

    OUTPUT:
    arcTan
    """
    
    distance = math.sqrt((firstPoint.X - endPoint.X)**2 + (firstPoint.Y - endPoint.Y)**2)

    return distance

def ArcTanBetween2points(firstPoint, endPoint):
    import math
    """Calculate arc tan between two points.

    INPUTS:
    first point, end point

    OUTPUT:
    arcTan
    """
    
    arcTan = math.atan2((firstPoint.X - endPoint.X),(firstPoint.Y - endPoint.Y))
    
    return arcTan

def RelativeDistance(Distance, Percent):
    """Calculate relative distance using percent.

    INPUTS:
    distance

    OUTPUT:
    50 percent of the distance
    """
    RelativeDistance = (float((Distance)) * float(Percent))/100
    
    return RelativeDistance

def GetFieldType(inFeatureClass, inFieldName):
    """Return field type: text or numeric

    INPUTS:
    Feature class and field

    OUTPUT:
    Return String for field TXT and LONG for numeric
    """
    # Process: get field type
    ListFieldString = ["String"]
    ListFieldFloat = ["SmallInteger", "Integer", "Single", "Double", "OID"]
    FieldType =""
    fields = arcpy.ListFields(inFeatureClass)
    for field in fields:
        if field.name == inFieldName:
            if field.type in ListFieldString:
                FieldType = "TEXT"
            elif field.type in ListFieldFloat:
                FieldType = "LONG"
    
        
    return FieldType


def do_analysis(inCenter,inFieldCenter,inBorder,inFieldBorder,inDimension,outFile):
    """TODO: Add documentation about this function here"""
    try:
        #TODO: Add analysis here
        arcpy.AddMessage("*"*10)
        arcpy.AddMessage("Process: Spider ...")
        
        # Process: Get input spatial reference
        sr = arcpy.Describe(inCenter).spatialreference
        
        # Process: Get field OBJECTID of 2 input layer
        OIDCenter = arcpy.Describe(inCenter).OIDFieldName
        OIDBorder = arcpy.Describe(inBorder).OIDFieldName
        
        # Process: Get field SHAPE
        SHPCenter = arcpy.Describe(inCenter).shapeFieldName
        SHPBorder = arcpy.Describe(inBorder).shapeFieldName
        
        # Process: Create output feature class...
        arcpy.CreateFeatureclass_management(os.path.dirname(outFile), os.path.basename(outFile), "POLYLINE", "", "DISABLED", "DISABLED", sr, "", "0", "0", "0")
        
        # Process: Add fields
        inFieldType = GetFieldType(inCenter, inFieldCenter)
        arcpy.AddField_management(outFile, "ID_CENTER", "LONG")
        arcpy.AddField_management(outFile, "ID_LINK", inFieldType)
        arcpy.AddField_management(outFile, "ID_BORDER", "LONG")
        
        # Process: Insert geometry in line layer
        iCursors = arcpy.InsertCursor(outFile, sr)
        
        # Process: Search center points
        sCursorsCen = arcpy.SearchCursor(inCenter)
        for sCursorCen in sCursorsCen:
            
            # Process: Get first point
            featCenter = sCursorCen.getValue(SHPCenter)
            pntCenter = featCenter.getPart()
            #gp.AddMessage("Xd %s - Yd %s" % (str(pntCenter.x), str(pntCenter.y)))
                    
            # Process: Prepare sql query
            delimitedfield = arcpy.AddFieldDelimiters(inBorder, inFieldBorder)
            sCursorsSel = arcpy.SearchCursor(inBorder, delimitedfield + " = " + str(sCursorCen.getValue(inFieldCenter)))
    
            for sCursorSel in sCursorsSel:
                # Process: Get end point
                featBorder = sCursorSel.getValue(SHPBorder)
                pntBorder = featBorder.getPart()
                #gp.AddMessage("Xf %s - Yf %s" % (str(pntBorder.x), str(pntBorder.y)))
                    
                # Process: Create line
                iCursor = iCursors.newRow()
                
                if int(inDimension) != 100:
                    # Process: Get line length
                    dist = DistanceBetween2Points(pntCenter, pntBorder)
                    
                    # Process: Get x percent of length
                    distBranche = RelativeDistance(dist, int(inDimension))
                    
                    # Process: get arc tan of the line
                    valeurArcTan = ArcTanBetween2points(pntCenter, pntBorder)
                    
                    # Process: Create relative line
                    iLine = CreateLineUsingPoint(pntCenter, valeurArcTan, distBranche)
                else:
                    # Process: Create line
                    iLine = CreateLine(pntCenter, pntBorder)
                
                # Process: store line
                iCursor.setValue("Shape",iLine)
                iCursor.setValue("ID_CENTER",sCursorCen.getValue(OIDCenter))
                iCursor.setValue("ID_LINK",sCursorCen.getValue(inFieldCenter))
                iCursor.setValue("ID_BORDER",sCursorSel.getValue(OIDBorder))
                iCursors.insertRow(iCursor)
                iLine.removeAll()
        
        # Clear variable
        del iCursors, sCursorsCen, sCursorCen, sCursorsSel, sCursorSel
    
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    finally:
        arcpy.AddMessage("end process")
        arcpy.AddMessage("*"*10)
# End do_analysis function

if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    print argv
    do_analysis(*argv)
