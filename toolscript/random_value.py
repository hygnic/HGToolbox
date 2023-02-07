# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              random_value
# Author:            Hygnic
# Created on:        2022/12/29 17:53
# Version:           
# Reference:         
"""
Description:         字段随机赋值，可限制范围，可选择小数或者整数 (以后再弄)
Usage:               
"""
# -------------------------------------------
import arcpy
import random
import os

# Input layer file
lyr = "xx"

# field
field = "f"

# expression
expression = "expression"


arcpy.CalculateField_management("vegtable.dbf", "VEG_TYP2",
                                '!VEG_TYPE!.split(" ")[-1]', "PYTHON_9.3")

