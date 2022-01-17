# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              merge_all_of_all
# Author:            Hygnic
# Created on:        2021/11/30 16:49
# Version:           
# Reference:         
"""
Description:         将一个（多个）图层合并成一个图层
                    并融合成一整块，消除所有重叠和属性信息
Usage:               
"""
# -------------------------------------------
#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>
from __future__ import absolute_import
import arcpy
import sys
import os

#------------添加环境变量
Script_dir = os.path.dirname(__file__)
Base_dir = os.path.dirname(Script_dir)
Libs_dir = os.path.join(Base_dir, "libs")
sys.path.append(Libs_dir)
#------------

import ezarcpy2
#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>
layers = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True
ezarcpy2.merger_all_layers(layers, output)
