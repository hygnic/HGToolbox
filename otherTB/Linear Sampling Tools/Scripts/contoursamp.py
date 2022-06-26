'''----------------------------------------------------------------------------------
 Tool Name:   Contour Sampling
 Source Name: contoursamp.py
 Author:      Vini Indriasari
 Required Arguments:
              Input contour feature class
              Output sample points feature class
              Total number of sample points
              Distribution of sample points across contour lines
              Interval of sample points
 Description: Generate sample points along contour lines.
 Date:        January 2014
----------------------------------------------------------------------------------'''

import arcpy
import random

# workspace for temporary fc
from arcpy import env
env.workspace = "C:/temp"
#env.workspace = arcpy.GetSystemEnvironment("TEMP")
env.overwriteOutput = True

#####################################################################################
# Parameters
#####################################################################################

# Input feature class containing contour lines
infc = arcpy.GetParameterAsText(0)

# Output feature class to store sample points
sampfc = arcpy.GetParameterAsText(1)

# Total number of sample points
numsamps = arcpy.GetParameter(2)

# Distribution of sample points across contour lines:
# Random, Uniform, Proportional
alloc = arcpy.GetParameterAsText(3)

# Interval of sample points along a given contour line:
# Random, Regular
space = arcpy.GetParameterAsText(4)

#####################################################################################
# Generate sample points
#####################################################################################

# Function to create sample points along a given contour line
def CreatePts(space, ns, con):
  pts = []
  
  # Place sample points at random interval along a contour line
  if space == "Random":
    for j in range(ns):
      d = random.uniform(0, con.length)
      pg = con.positionAlongLine(d)
      pts.append(pg)
      
  if space == "Regular":
  # Place sample points at regular interval along a contour line
    if ns > 0:
      sp = con.length / ns
      d = sp/2
    else:
      sp = 0
      
    for j in range(ns):
      pg = con.positionAlongLine(d)
      pts.append(pg)
      d += sp
    
  return pts

# Calculate number of contour lines
numcons = int(arcpy.GetCount_management(infc).getOutput(0))

# Calculate total length of contour lines
cur = arcpy.da.SearchCursor(infc, (["SHAPE@"]))
totLength = 0
contours = []
for row in cur:
  ft = row[0]
  totLength += ft.length
  contours.append(ft)
del cur

samp = []
# (1) Random  
if alloc == "Random":
  # Assign sample points randomly to contour lines
  asg = []
  for i in range(numsamps):
    asg.append(random.randrange(numcons))
    
  # Create sample points along each contour line  
  for j in range(numcons):
    ns = asg.count(j) # number of points at contour line
    con = contours[j] # contour line geometry
    samp.extend(CreatePts(space, ns, con))
    
# (2) Uniform
elif alloc == "Uniform":
  # Assign sample points to contour lines in an orderly manner
  asg = []
  for i in range(numsamps):
    asg.append(i%numcons)
    
  # Create sample points along each contour line
  for j in range(numcons):
    ns = asg.count(j) # number of points at contour line
    con = contours[j] # contour line geometry
    samp.extend(CreatePts(space, ns, con))
    
# (3) Proportional
else:
  # Calculate point density (sample points per unit length)
  ptDen = numsamps/totLength

  # Create sample points along each contour line
  for con in contours:
    ns = int(round(ptDen * con.length)) # number of points at contour line
    samp.extend(CreatePts(space, ns, con))
  # Some contour lines may not long enough to get any sample point
    
if any(samp):
  arcpy.CopyFeatures_management(samp, sampfc)
else:
  arcpy.AddError("No sample points created.")
