#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:33:48 2022

@author: dan
"""


import os
import sys

sys.path.append('wma_pyTools')
startDir=os.getcwd()
#some how set a path to wma pyTools repo directory
#wmaToolsDir='wma_pyTools'
#wmaToolsDir='..'
#os.chdir(wmaToolsDir)
print(os.getcwd())
print(os.listdir())
import wmaPyTools.roiTools
import wmaPyTools.analysisTools
import wmaPyTools.segmentationTools
import wmaPyTools.streamlineTools
import wmaPyTools.visTools
import wmaPyTools.genUtils

#os.chdir(startDir)

import os
import json
import numpy as np
import nibabel as nib
import pandas as pd


# load inputs from config.json
with open('config.json') as config_json:
	config = json.load(config_json)

outDirParc='output_parc'
if not os.path.exists(outDirParc):
    os.makedirs(outDirParc)

outIslandDirCSV='output_islandcsv'
if not os.path.exists(outIslandDirCSV):
    os.makedirs(outIslandDirCSV)
    
outInflateDirCSV='output_inflatecsv'
if not os.path.exists(outInflateDirCSV):
    os.makedirs(outInflateDirCSV)

parcIn=nib.load(config['parc'])
inflateParam=config['inflate']
#inferWMParam=config['inferWM']
retainOrigBorders=config['retainOrigBorders']
maintainIslandsLabels=config['maintainIslandsLabels']
erodeLabels=config['erodeLabels']

outParc,deIslandReport,inflationReport=wmaPyTools.roiTools.preProcParc(parcIn,deIslandBool=True,inflateIter=inflateParam,retainOrigBorders=retainOrigBorders,maintainIslandsLabels=maintainIslandsLabels,erodeLabels=erodeLabels)

nib.save(outParc,os.path.join(outDirParc,'parc.nii.gz'))

deIslandReport.to_csv(os.path.join(outIslandDirCSV,'de-island_report.csv'))
inflationReport.to_csv(os.path.join(outInflateDirCSV,'inflate_report.csv'))
