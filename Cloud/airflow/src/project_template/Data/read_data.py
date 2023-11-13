"""
This module provides the read_data function, which is utilized by the pipeline orchestrator (Airflow) for data ingestion.
The function implements the logic to ingest the data and transform it into a pandas format. If any additional auxiliary
functions are required to accomplish this step, they can be defined within the same script or separated into different
scripts and included in the Data directory.
"""

#import requests
import pandas as pd
from minio import Minio

def read_data() -> pd.DataFrame:
    """
    The function implements the logic to ingest the data and transform it into a pandas format.

    Return:
        A Pandas DataFrame representing the content of the specified file.
    """

    # ADD YOUR CODE HERE
    url = "localhost:9000"
    bucket = "mlflow"

    client = Minio(
        url,
        access_key="user",
        secret_key="password",
        secure=False
    )

    obj = client.get_object(
        bucket,
        "turndataset.csv",
    )
    return pd.read_csv(obj, index_col=0)

a = read_data()
print(a)
