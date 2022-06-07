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
import shutil

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
deIslandBool=config['deisland']
inflateParam=config['inflate']
#inferWMParam=config['inferWM']
retainOrigBorders=config['retainOrigBorders']
maintainIslandsLabels=config['maintainIslandsLabels']
#check case for empty input
if maintainIslandsLabels == '':
    maintainIslandsLabels=[]
erodeLabels=config['erodeLabels']
#check case for empty input
if erodeLabels == '':
    erodeLabels=[]

outParc,deIslandReport,inflationReport=wmaPyTools.roiTools.preProcParc(parcIn,deIslandBool=deIslandBool,inflateIter=inflateParam,retainOrigBorders=retainOrigBorders,maintainIslandsLabels=maintainIslandsLabels,erodeLabels=erodeLabels)

nib.save(outParc,os.path.join(outDirParc,'parc.nii.gz'))
shutil.copyfile(config['label'], os.path.join(outDirParc,'label.json'))

outDirParcStats='parc-stats'
if not os.path.exists(os.path.join(outIslandDirCSV,outDirParcStats)):
    os.makedirs(os.path.join(outIslandDirCSV,outDirParcStats))
if not os.path.exists(os.path.join(outInflateDirCSV,outDirParcStats)):
    os.makedirs(os.path.join(outInflateDirCSV,outDirParcStats))   
deIslandReport.to_csv(os.path.join(outIslandDirCSV,'parc-stats','de-island_report.csv'))
inflationReport.to_csv(os.path.join(outInflateDirCSV,'parc-stats','inflate_report.csv'))
