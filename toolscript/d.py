# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              d
# Author:            Hygnic
# Created on:        2022/5/26 14:19
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
arcpy.env.Overw

Data_Input = arcpy.GetParameterAsText(0) #Excel or table
FCPoint_Name = arcpy.GetParameterAsText(1)
X_Coord = arcpy.GetParameterAsText(2)
Y_Coord = arcpy.GetParameterAsText(3)

#New field option
value_table = arcpy.ValueTable(3)#Value table
New_Field = value_table.loadFromString(arcpy.GetParameterAsText(4))

#Excel output option
Excel_Output = arcpy.GetParameterAsText(5)


##excel conversion
if Data_Input =='File':
    arcpy.ExcelToTable_conversion(Data_Input, "Table_Name", "Sheet1")
    arcpy.MakeTableView_management("Table_Name", "out_view")
    # arcpy.management.XYTableToPoint("out_view", FCPoint_Name, X_Coord, Y_Coord)
    arcpy.MakeXYEventLayer_management("out_view", X_Coord, Y_Coord, "in_memory/out_Layer")
    arcpy.Copy_management("in_memory/out_Layer","FCPoint_Name")

#Table input
else:
    arcpy.MakeTableView_management(Data_Input, "out_view")
    # arcpy.management.XYTableToPoint("out_view", FCPoint_Name, X_Coord, Y_Coord)
    arcpy.MakeXYEventLayer_management("out_view", X_Coord, Y_Coord, "in_memory/out_Layer")
    arcpy.Copy_management("in_memory/out_Layer","FCPoint_Name")
    
#Add/Calculate fields (Optional)
if New_Field == '':
    print("next")

else:
    
    for i in range(0, value_table.rowCount):
        Field_Name = value_table.getValue (i, 0)
        Field_Type = value_table.getValue (i, 1)
        Expression =value_table.getValue (i, 2)
        New_name = arcpy.ValidateFieldName(Field_Name)
        field_names = [f.name for f in arcpy.ListFields(FCPoint_Name)]
        if New_name in field_names:
            arcpy.AddError(Field_Name+" field name already exists")
        else:
            arcpy.AddField_management(FCPoint_Name, New_name, Field_Type)
            arcpy.CalculateField_management(FCPoint_Name, New_name, Expression, "ARCADE")


#Save as excel file (Optional)
if Excel_Output == '':
    print("next")
else:
    arcpy.MakeTableView_management(FCPoint_Name, "Excel_view")
    arcpy.conversion.TableToExcel("Excel_view", Excel_Output)




