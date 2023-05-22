import os
import pandas as pd
from pathlib import Path
import uuid
import json
import numpy as np
import shutil

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')


def generateInputs(dataset_uri):
    '''
    Function to generate desired inputs for SCODE.
    If the folder/files under RunnerObj.datadir exist, 
    this function will not do anything.
    '''
    expressionDataPath = os.path.join(DATASET_PATH, dataset_uri)

    os.makedirs("/tmp/", exist_ok=True) # Create the /tmp/ directory if it doesn't exist
    uniqueID = str(uuid.uuid4())
    tempUniqueDirPath = "/tmp/" + uniqueID
    os.makedirs(tempUniqueDirPath, exist_ok=True)
    
    ExpressionData = pd.read_csv(expressionDataPath, header=0, index_col=0)
    ExpressionData.to_csv(tempUniqueDirPath + "/ConvertedExpressionData.csv", sep = '\t', header  = True, index = True)
    return tempUniqueDirPath
    
def run(tempUniqueDirPath):
    '''
    Function to run PIDC algorithm
    '''
    outPath = tempUniqueDirPath + '/outFile.txt'

    cmdToRun = ' '.join(['julia runPIDC.jl', tempUniqueDirPath + "/ConvertedExpressionData.csv", outPath])
    print(cmdToRun)
    os.system(cmdToRun)

    return tempUniqueDirPath

def parseOutput(tempUniqueDirPath):
    '''
    Function to parse outputs from SCODE.
    ''' 
    # Read output
    OutDF = pd.read_csv(tempUniqueDirPath+'/outFile.txt', sep = '\t', header = None)

    results = {'Gene1': [], 
               'Gene2': [],
               'EdgeWeight': []}

    for idx, row in OutDF.iterrows():
        results['Gene1'].append(row[0])
        results['Gene2'].append(row[1])
        results['EdgeWeight'].append(str(row[2]))

    shutil.rmtree(tempUniqueDirPath)
    
    return json.dumps(results)
    
