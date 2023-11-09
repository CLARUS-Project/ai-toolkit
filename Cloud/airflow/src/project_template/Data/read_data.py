"""
This module provides the read_data function, which is utilized by the pipeline orchestrator (Airflow) for data ingestion.
The function implements the logic to ingest the data and transform it into a pandas format. If any additional auxiliary
functions are required to accomplish this step, they can be defined within the same script or separated into different
scripts and included in the Data directory.
"""

#import requests
import pandas as pd
import json
from io import StringIO
from os.path import abspath

PATH = abspath('Data/turndataset.csv')

def read_data() -> pd.DataFrame:
    """
    The function implements the logic to ingest the data and transform it into a pandas format.

    Return:
        A Pandas DataFrame representing the content of the specified file.
    """

    # ADD YOUR CODE HERE

    return pd.read_csv(PATH, index_col=0)

