import time
import mlflow
from mlflow.tracking.client import MlflowClient
from fastapi import FastAPI
from mlflow.pyfunc import load_model

import os
import zipfile
import io
import sklearn
import shutil
import numpy as np

MLFLOW_PATH=os.environ["MLFLOW_PATH"]
MLFLOW_EXPERIMENT=os.environ["MLFLOW_EXPERIMENT"]
AWS_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"]
MLFLOW_S3_ENDPOINT_URL=os.environ["MLFLOW_S3_ENDPOINT_URL"] 

# # Create the POST endpoint with path '/predict'
app = FastAPI()
@app.get("/predict")
def deploy_model_predict(datos,model):

    client = MlflowClient(MLFLOW_PATH)
    mlflow.set_tracking_uri(MLFLOW_PATH)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    

    print('Modelo utilizado para calcular predicciones: ', model)
    model = f'runs:/{model}/model'
    model = load_model(model)

    trans_data = np.array([*eval(datos).values()]).reshape(1,-1)

    pred_model = model.predict(trans_data)[0]
    print('Predicción del modelo: ', pred_model)
    return float(pred_model)
    


