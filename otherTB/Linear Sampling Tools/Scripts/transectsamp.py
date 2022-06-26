'''----------------------------------------------------------------------------------
 Tool Name:   Transect Sampling
 Source Name: transectsamp.py
 Author:      Vini Indriasari
 Required Arguments:
              Input line feature class
              Output sample points feature class
              Spacing between transect lines
              Width of transect lines
              Direction to generate transect lines
              Number of sample points per transect line
 Optional Argument:
              Create transect line feature class
 Description: Generate transect lines along the lines, and then generate sample
              points along each transect line.
 Date:        January 2014
 Updated:     January 2018 (fixing zero dividion in calculating slope of line segment
----------------------------------------------------------------------------------'''

import arcpy
import os
import math

# workspace for temporary fc
from arcpy import env
env.workspace = "C:/temp"
#env.workspace = arcpy.GetSystemEnvironment("TEMP")
env.overwriteOutput = True

#####################################################################################
# Parameters
#####################################################################################

# Input feature class containing linear features
infc = arcpy.GetParameterAsText(0)

# Output feature class to store sample points
sampfc = arcpy.GetParameterAsText(1)
dirfc = os.path.dirname(sampfc)
filefc = os.path.basename(sampfc)

# Spacing between transect lines
sp = arcpy.GetParameter(2)

# Width of transect lines
fwi = arcpy.GetParameter(3)

# Direction to generate transect lines: FT, TF
flow = arcpy.GetParameterAsText(4)
# FT (From-To): in digitized direction of the line
# TF (To-From): against digitized direction of the line

# Option to create transect lines fc
tranopt = arcpy.GetParameter(5)

# Number of sample points per transect line
numTranPts = arcpy.GetParameter(6)

#####################################################################################
# Generate transect lines
#####################################################################################

################################ Create cross points ################################
# Create cursor to search stream features
cur = arcpy.da.SearchCursor(infc, (["SHAPE@"]))

crPts = [] # list of cross points along the stream
for row in cur:
  # Get stream geometry from cursor
  stream = row[0] # Polyline
  
  if flow.upper() == "FT":
    # Define a position on the stream where to stop generating cross points
    dmax = stream.length
    d = 0 # distance d starts from the start point of the line
      
    # Create cross points along the stream at regular interval
    while d < dmax:
      # Get position of a point at distance d
      cross = stream.positionAlongLine(d) # PointGeometry
      crPts.append(cross) # add cross point into the list
      d += sp # increase the distance by spacing
      
  else: # flow = TF
    # Define a position on the stream where to stop generating cross points
    dmin = 0
    d = stream.length # distance d starts from the end point of the line
      
    # Create cross points along the stream at regular interval
    while d > dmin:
      # Get position of a point at distance d
      cross = stream.positionAlongLine(d) # PointGeometry
      crPts.append(cross) # add cross point into the list
      d -= sp # decrease the distance by spacing
      
del cur # delete cursor

# Get spatial reference of input feature class
desc = arcpy.Describe(infc) 
sr = desc.spatialReference
  
############################### Create transect lines ###############################
crLines = [] # list of cross lines along the stream
# Split stream at vertices to get individual line segments
segments = arcpy.SplitLine_management(infc, arcpy.Geometry())

# Loop through cross points
for cross in crPts:
  # Get Point class of cross point
  pt = cross.firstPoint # Point
  
  # Get X,Y coord of cross point
  xC = pt.X
  yC = pt.Y
  
  # Find line segment overlapping with cross point
  for seg in segments:
    if seg.contains(pt) or seg.touches(pt):
      # Get the start and end points of line segment
      fr = seg.firstPoint
      to = seg.lastPoint
      
      # Calculate the slope of line segment
      rise = to.Y - fr.Y
      run = to.X - fr.X
      if run == 0: # handle zero division
          a = math.radians(90)
      else:  
          # Calculate the slope angle
          slope = rise/run
          a = math.atan(slope) # in radian
      
      # Find dx and dy to get vector wi at angle a
      wi = fwi/2 # half width of cross line
      dx = wi * math.cos(a)
      dy = wi * math.sin(a)
      
      # Rotate vector wi +90 deg around cross point
      xOri = xC + dy
      yOri = yC - dx
      
      # Rotate vector wi -90 deg around cross point
      xDes = xC - dy
      yDes = yC + dx
      
      # Determine origin and destination points of cross line
      ori = arcpy.Point(xOri,yOri)
      des = arcpy.Point(xDes,yDes)
      
      # Add origin and destination points into an array object
      arr = arcpy.Array()
      arr.add(ori)
      arr.add(des)
      
      # Contruct a cross line from the array object
      line = arcpy.Polyline(arr, sr)
      
      # Add the cross line into the list
      crLines.append(line)
      
      break # no need to check the remaining line segments

# Create transect lines fc
if any(crLines) and (tranopt):
  f = os.path.splitext(filefc) # split into file and extension
  trannm = f[0] + "_transects" + f[1] # transect basename
  tranfc = os.path.join(dirfc, trannm)
  arcpy.CopyFeatures_management(crLines, tranfc)
  arcpy.SetParameterAsText(7, tranfc)

#####################################################################################
# Generate sample points
#####################################################################################
if any(crLines):
  # Calculate spacing between sample points along transect line
  ds = fwi / numTranPts
  
  # Create sample points along each transect line
  samp = []
  for line in crLines:
    d = ds/2 # starting point
    for i in range(numTranPts):
      pg = line.positionAlongLine(d)
      samp.append(pg)
      d += ds
      
  if any(samp):
    arcpy.CopyFeatures_management(samp, sampfc)
  else:
    arcpy.AddError("No sample points created.")
else:
  arcpy.AddError("No transect lines created.")
  
