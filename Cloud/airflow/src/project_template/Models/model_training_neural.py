"""
This module defines the `model_training` function used by the pipeline orchestrator to train a machine 
learning model using ElasticNet regularization. This function defines the logic for training the model and evaluating 
its performance.

Any additional functions or utilities required for this step can be defined within this script itself or split into 
different scripts and included in the Process directory.
"""

from typing import Dict, Any
from sklearn.linear_model import ElasticNet
from datetime import datetime
from Models import utils
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
#import tensorflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from urllib.parse import urlparse
import numpy as np
import config
from mlflow.tracking.client import MlflowClient
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def model_training_neural(data: Dict[str, Any]):
    """Neural net training"""
    try:
        install("tensorflow==2.10.1")
        install("protobuf==3.19.6")
    except Exception as err:
        print(err)
    pass
    import tensorflow
    """
    Args:
        data: A dictionary containing the preprocessed data.

    Returns:
        None
    """

    # ADD YOUR CODE HERE: READ INPUT DATA
    # ADD YOUR CODE HERE: TRAIN THE MODEL
    # ADD YOUR CODE HERE: DO NOT FORGET TO TRACK THE MODEL TRAINING
    inp_len = len(data["dataset1_x_train"][0])
    x_train = np.array(data["dataset1_x_train"])
    x_train = x_train.reshape(-1, 1, inp_len)
    y_train = np.array(data["dataset1_y_train"])
    y_train = y_train.reshape(-1, 1, 1)

    x_test = np.array(data["dataset1_x_test"])
    x_test = x_test.reshape(-1, 1, inp_len)
    y_test = np.array(data["dataset1_y_test"])
    y_test = y_test.reshape(-1, 1, 1)
    # Hidden layer with a lot more feature extraction neurons


    client = MlflowClient(config.MLFLOW_ENDPOINT)
    mlflow.set_tracking_uri(config.MLFLOW_ENDPOINT)
    try:
        mlflow.set_experiment(config.MLFLOW_EXPERIMENT)
    except:
        time.sleep(10)
        mlflow.set_experiment(config.MLFLOW_EXPERIMENT)
    with mlflow.start_run(run_name="Bidirectional-LSTM"):
        regr = tensorflow.keras.models.Sequential()
        regr.add(tensorflow.keras.layers.Input(shape=(1,inp_len)))
        dropout_rate = 0.1
        layer1_neur = 100
        layer2_neur = 100
        epoch_num = 1
        regr.add(tensorflow.keras.layers.Bidirectional(tensorflow.keras.layers.LSTM(layer1_neur,input_shape=(1,inp_len), return_sequences=True,dropout=dropout_rate,activation="swish")))
        regr.add(tensorflow.keras.layers.Bidirectional(tensorflow.keras.layers.LSTM(layer2_neur,dropout=dropout_rate,activation="swish")))
        regr.add(tensorflow.keras.layers.Dense(1))

        optimizer = tensorflow.keras.optimizers.Adam()

        print(regr.summary())
        regr.compile(optimizer=optimizer, loss=tensorflow.keras.losses.MeanSquaredError(), metrics=tensorflow.keras.metrics.MeanAbsoluteError())
        history = regr.fit(x_train, y_train, epochs=epoch_num)
        regr.fit(x_train, y_train)

        pred_values = regr.predict(x_test)

        (rmse, mae, r2) = utils.eval_metrics_2(data["dataset1_y_test"], pred_values)

        print(f"NN model bidirectional LSTM (layer1={layer1_neur:f}, layer2={layer2_neur:f},dropout={dropout_rate},epoch={epoch_num:f}):")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        mlflow.log_param("layer_type", "bidirectional LSTM")
        mlflow.log_param("layer1_neur_number", layer1_neur)
        mlflow.log_param("layer2_neur_number", layer2_neur)
        mlflow.log_param("dropout_rate", dropout_rate)
        mlflow.log_param("epoch", epoch_num)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        predictions = regr.predict(x_train)
        signature = infer_signature(x_train, np.array(predictions))

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":
            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                regr, "model", registered_model_name="Bidirectional-LSTM", signature=signature
            )
        else:
            mlflow.sklearn.log_model(regr, "model", signature=signature)

    pass
