"""
This module defines the `select_best_model` function used by the pipeline orchestrator to select the best model 
from an MLflow experiment based on a specified metric.

This function connects to the MLflow tracking server and retrieves the best model based on the specified metric 
from the MLflow experiment. The metric can be either maximized or minimized based on the provided metric type. 
Once the best model is identified, it can be transitioned to the Production stage.

Any additional functions or utilities required for this step can be defined within this script itself or split 
into different scripts and included in the Process directory.
"""

import mlflow
from mlflow.tracking.client import MlflowClient
import config
import numpy as np

def select_best_model():
    """
    Select the best model based on a specified metric from the MLflow experiment.

    This function connects to the MLflow tracking server using the provided endpoint. It retrieves the best model
    based on the specified metric from the MLflow experiment. The metric can be either maximized or minimized based
    on the provided metric type. Once the best model is identified, it can be transitioned to the Production stage.

    Returns:
        None
    """

    endpoint = config.MLFLOW_ENDPOINT
    experiment = config.MLFLOW_EXPERIMENT
    metric = config.METRIC_BM
    metric_type = config.METRIC_BM_TYPE

    client = MlflowClient(endpoint)
    mlflow.set_tracking_uri(endpoint)
    mlflow.set_experiment(experiment)

    runs_lookback = 5

    # ADD YOUR CODE HERE

    # Retrieve the best model based on the specified metric
    if metric_type=='max':
        runs = client.search_runs(experiment_ids=client.get_experiment_by_name(experiment).experiment_id,
                                 order_by=[f"metrics.{metric} DESC"],max_results=runs_lookback)
    else:
         runs = client.search_runs(experiment_ids=client.get_experiment_by_name(experiment).experiment_id,
                                 order_by=[f"metrics.{metric} ASC"],max_results=runs_lookback)

    runs_info = [[run.data.metrics['Validation concordance index ipcw'], run.data.metrics['mean auc'], run.data.metrics['test integrated brier score']] for run in runs]
    runs_info = np.array(runs_info, dtype=[('Validation concordance index ipcw', float), ('mean auc', float), ('test integrated brier score', float)])
    run_points = (runs_info['Validation concordance index ipcw'] + runs_info['mean auc'])/2 - runs_info['test integrated brier score']
    best_run = runs[run_points.argmax()].info.run_id
    print(f'BEST RUN: {best_run}')

    #CHANGE STATE TO PRODUCTION
    best_model = runs[0].data.tags.get("mlflow.runName")
    model_version = client.get_latest_versions(best_model)[0]

    #Transition to Production of the best model obtained
    client.transition_model_version_stage(name=best_model, version=model_version.version,stage="Production")
