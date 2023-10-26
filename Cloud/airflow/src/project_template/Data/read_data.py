"""
This module provides the read_data function, which is utilized by the pipeline orchestrator (Airflow) for data ingestion. 
The function implements the logic to ingest the data and transform it into a pandas format. If any additional auxiliary 
functions are required to accomplish this step, they can be defined within the same script or separated into different 
scripts and included in the Data directory.
"""

import requests
import pandas as pd
import json
from io import StringIO
import sys
import config
import subprocess
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def read_data():
    try:
        install("openpyxl")
    except:
        pass
    """
    The function implements the logic to ingest the data and transform it into a pandas format.

    Return:
        A Pandas DataFrame representing the content of the specified file.
    """
    dataframe_test= pd.DataFrame([])
    #sys.path.append("dags/")
    #dataframe_test.to_csv("target1.csv")
    #print("target saved 2")
    # ADD YOUR CODE HERE
    #sys.path.append("C:/Users/tktuvu/Desktop/ai-toolkit/Cloud/airflow/src/project_template/")

    #
    dataframe = pd.read_csv("dags/filtered_set2021tagged.csv")
    print(dataframe)
    return dataframe
