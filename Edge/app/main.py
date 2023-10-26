import json
import time
import mlflow
from mlflow.tracking.client import MlflowClient
from fastapi import FastAPI
from mlflow.pyfunc import load_model, save_model

import os
import zipfile
import io
import sklearn
import shutil
import numpy as np
import boto3
MLFLOW_PATH=os.environ["MLFLOW_PATH"]
MLFLOW_EXPERIMENT=os.environ["MLFLOW_EXPERIMENT"]
AWS_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"]
MLFLOW_S3_ENDPOINT_URL=os.environ["MLFLOW_S3_ENDPOINT_URL"]

#MLFLOW_PATH = "http://localhost:5000"
#MLFLOW_EXPERIMENT="Clarus_template_experiment"
#AWS_ACCESS_KEY_ID = "user"
#AWS_SECRET_ACCESS_KEY="password"
#MLFLOW_S3_ENDPOINT_URL="http://localhost:9000"
#log in

client = MlflowClient(MLFLOW_PATH)
mlflow.set_tracking_uri(MLFLOW_PATH)
mlflow.set_experiment(MLFLOW_EXPERIMENT)
# # Create the POST endpoint with path '/predict'

try:
    model = load_model(model_uri=f"models:/RFRModel/1")
except:
    model = None

app = FastAPI()


@app.get("/model_loading")
def load_model_from_api(data_package):
    global model
    """
    load model
    """
    data_decoded = json.loads(data_package)
    model_info = data_decoded["model"]
    model_data = model_info.split("/")
    model = load_model(model_uri=f"models:/{model_data[0]}/{model_data[1]}")
    #save_model("imported_model", python_model=model)
    return "model_loaded"


@app.get("/predict")
def deploy_model_predict(data_package):
    global model
    """
    The function implements the logic to do the inference.
    """
    # ADD YOUR CODE HERE
    data_decoded = json.loads(data_package)
    datos = data_decoded["datos"]
    print("data",datos)

    inp_data = np.array(datos).reshape(-1,len(datos))

    result_preded = model.predict(inp_data)
    print(result_preded)
    return_dict = {"predicted_data":result_preded.tolist()}
    return return_dict

#import uvicorn
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=381)
